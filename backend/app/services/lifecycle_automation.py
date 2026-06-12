from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.opportunity import OpportunityStatus
from app.repositories.opportunity import OpportunityRepository, LifecycleRepository
from app.services.audit import AuditService

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


class LifecycleAutomation:
    def __init__(self):
        self.opp_repo = OpportunityRepository()
        self.lifecycle_repo = LifecycleRepository()
        self.audit = AuditService()

    def _stage_index(self, status: str) -> int:
        try:
            return LIFECYCLE_FLOW.index(status)
        except ValueError:
            return -1

    def advance_to(self, db: Session, site_id, target_status: str, user: User, remarks: str):
        opps = self.opp_repo.get_by_site(db, site_id)
        if not opps:
            return None
        opp = opps[0]
        current = opp.current_status
        if current == OpportunityStatus.LOST.value:
            return None
        target_idx = self._stage_index(target_status)
        current_idx = self._stage_index(current)
        if target_idx < 0 or current_idx < 0 or target_idx <= current_idx:
            return opp

        self.opp_repo.update(db, opp, {"current_status": target_status})
        now = datetime.now(timezone.utc)
        self.lifecycle_repo.create(db, {
            "opportunity_id": opp.id,
            "previous_status": current,
            "new_status": target_status,
            "changed_by": user.id,
            "changed_at": now,
            "remarks": remarks,
        })
        self.audit.log(
            db, user_id=user.id, entity_type="opportunity", entity_id=opp.id,
            action="auto_transition", previous_value={"status": current}, new_value={"status": target_status},
        )
        return self.opp_repo.get(db, str(opp.id))
