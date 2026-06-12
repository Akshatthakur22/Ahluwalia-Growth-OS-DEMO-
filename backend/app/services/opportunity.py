from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, Role, EmploymentStatus
from app.models.opportunity import OpportunityStatus
from app.repositories.opportunity import OpportunityRepository, LifecycleRepository, OwnershipRepository
from app.repositories.site import SiteRepository
from app.schemas.opportunity import OpportunityCreate, OpportunityUpdate, OpportunityTransition, LeadTransferRequest
from app.services.audit import AuditService
from app.services.lifecycle_automation import LifecycleAutomation


LIFECYCLE_FLOW = [
    OpportunityStatus.NEW_SITE.value,
    OpportunityStatus.RELATIONSHIP_BUILDING.value,
    OpportunityStatus.SHOWROOM_VISIT_SCHEDULED.value,
    OpportunityStatus.SHOWROOM_VISIT_DONE.value,
    OpportunityStatus.SELECTION_DONE.value,
    OpportunityStatus.QUOTATION_SENT.value,
    OpportunityStatus.NEGOTIATION.value,
    OpportunityStatus.ORDER_CONFIRMED.value,
]

ACTIVE_STATES = LIFECYCLE_FLOW + [OpportunityStatus.LOST.value]


class OpportunityService:
    def __init__(self):
        self.repo = OpportunityRepository()
        self.lifecycle_repo = LifecycleRepository()
        self.ownership_repo = OwnershipRepository()
        self.site_repo = SiteRepository()
        self.audit = AuditService()
        self.lifecycle = LifecycleAutomation()

    def _can_transition(self, current: str, new: str, user: User) -> bool:
        if user.role in (Role.MANAGER, Role.ADMINISTRATOR):
            return True
        if new == OpportunityStatus.LOST.value:
            return user.role in (Role.MARKETING_EXECUTIVE, Role.SALES_EXECUTIVE, Role.MANAGER)
        if current == OpportunityStatus.NEW_SITE.value and new == OpportunityStatus.RELATIONSHIP_BUILDING.value:
            return user.role in (Role.MARKETING_EXECUTIVE, Role.MANAGER)
        marketing_states = {
            OpportunityStatus.RELATIONSHIP_BUILDING.value,
            OpportunityStatus.SHOWROOM_VISIT_SCHEDULED.value,
        }
        sales_states = {
            OpportunityStatus.SHOWROOM_VISIT_DONE.value,
            OpportunityStatus.SELECTION_DONE.value,
            OpportunityStatus.QUOTATION_SENT.value,
            OpportunityStatus.NEGOTIATION.value,
            OpportunityStatus.ORDER_CONFIRMED.value,
        }
        if new in marketing_states:
            return user.role in (Role.MARKETING_EXECUTIVE, Role.MANAGER)
        if new in sales_states:
            return user.role in (Role.SALES_EXECUTIVE, Role.MANAGER)
        if current in LIFECYCLE_FLOW and new in LIFECYCLE_FLOW:
            current_idx = LIFECYCLE_FLOW.index(current)
            new_idx = LIFECYCLE_FLOW.index(new)
            # Demo: allow forward-only jumps within same role lane (not backwards)
            if user.role in (Role.MARKETING_EXECUTIVE, Role.SALES_EXECUTIVE):
                return new_idx > current_idx
            return new_idx == current_idx + 1
        return False

    def create_opportunity(self, db: Session, user: User, data: OpportunityCreate):
        if not self.site_repo.get(db, str(data.site_id)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")
        opp_data = data.model_dump()
        opp_data["current_status"] = OpportunityStatus.NEW_SITE.value
        opportunity = self.repo.create(db, opp_data)
        self.ownership_repo.create(db, {"opportunity_id": opportunity.id, "lead_creator_id": user.id})
        self.audit.log(db, user_id=user.id, entity_type="opportunity", entity_id=opportunity.id, action="create", new_value=opp_data)
        return opportunity

    def list_opportunities(self, db: Session, skip: int = 0, limit: int = 100):
        return self.repo.get_multi(db, skip, limit)

    def get_opportunity(self, db: Session, opportunity_id: str):
        opp = self.repo.get(db, opportunity_id)
        if not opp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opportunity not found")
        return opp

    def update_opportunity(self, db: Session, user: User, opportunity_id: str, data: OpportunityUpdate):
        opp = self.get_opportunity(db, opportunity_id)
        update_data = data.model_dump(exclude_unset=True)
        updated = self.repo.update(db, opp, update_data)
        self.audit.log(db, user_id=user.id, entity_type="opportunity", entity_id=opp.id, action="update", new_value=update_data)
        return updated

    def transition(self, db: Session, user: User, opportunity_id: str, data: OpportunityTransition):
        opp = self.get_opportunity(db, opportunity_id)
        previous = opp.current_status
        new_status = data.new_status

        if not self._can_transition(previous, new_status, user):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Transition from {previous} to {new_status} not allowed")

        opp = self.repo.update(db, opp, {"current_status": new_status})
        now = datetime.now(timezone.utc)
        self.lifecycle_repo.create(db, {
            "opportunity_id": opp.id,
            "previous_status": previous,
            "new_status": new_status,
            "changed_by": user.id,
            "changed_at": now,
            "remarks": data.remarks,
        })
        self.audit.log(
            db, user_id=user.id, entity_type="opportunity", entity_id=opp.id,
            action="transition", previous_value={"status": previous}, new_value={"status": new_status},
        )
        return {"previous_status": previous, "new_status": new_status, "transition_timestamp": now}

    def get_lifecycle_history(self, db: Session, opportunity_id: str):
        self.get_opportunity(db, opportunity_id)
        return self.lifecycle_repo.get_by_opportunity(db, opportunity_id)

    def get_ownership(self, db: Session, opportunity_id: str):
        self.get_opportunity(db, opportunity_id)
        record = self.ownership_repo.get_by_opportunity(db, opportunity_id)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ownership record not found")
        return record

    def update_ownership(self, db: Session, user: User, opportunity_id: str, data: dict):
        if user.role not in (Role.MANAGER, Role.ADMINISTRATOR):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manager access required")
        self.get_opportunity(db, opportunity_id)
        record = self.ownership_repo.get_by_opportunity(db, opportunity_id)
        if not record:
            record = self.ownership_repo.create(db, {"opportunity_id": opportunity_id, **data})
        else:
            record = self.ownership_repo.update(db, record, data)
        self.audit.log(db, user_id=user.id, entity_type="ownership", entity_id=record.id, action="update", new_value=data)
        return record

    def lead_transfer(self, db: Session, user: User, opportunity_id: str, data: LeadTransferRequest):
        if user.role not in (Role.MARKETING_EXECUTIVE, Role.MANAGER, Role.ADMINISTRATOR):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Marketing access required")
        opp = self.get_opportunity(db, opportunity_id)
        ownership = self.ownership_repo.get_by_opportunity(db, opp.id)
        if not ownership:
            ownership = self.ownership_repo.create(db, {"opportunity_id": opp.id, "lead_creator_id": user.id})

        sales_users = db.query(User).filter(
            User.role == Role.SALES_EXECUTIVE, User.status == EmploymentStatus.ACTIVE
        ).all()
        if sales_users:
            self.ownership_repo.update(db, ownership, {"sales_owner_id": sales_users[0].id})

        transfer_note = (
            f"Lead transfer: visit {data.expected_visit_date.date()}, "
            f"qty {data.expected_quantity or 'TBD'}, priority {data.priority}. "
            f"{data.remarks or ''}"
        ).strip()
        opp_update = {"follow_up_date": data.expected_visit_date, "remarks": transfer_note}
        if data.expected_quantity:
            opp_update["quotation_value"] = data.expected_quantity
        self.repo.update(db, opp, opp_update)

        self.lifecycle.advance_to(
            db, opp.site_id, OpportunityStatus.SHOWROOM_VISIT_SCHEDULED.value, user,
            f"Lead transfer to sales — {transfer_note}",
        )
        self.audit.log(
            db, user_id=user.id, entity_type="opportunity", entity_id=opp.id,
            action="lead_transfer", new_value=data.model_dump(mode="json"),
        )
        return self.get_opportunity(db, opportunity_id)
