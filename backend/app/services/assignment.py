from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, Role
from app.repositories.assignment import AssignmentRepository
from app.repositories.site import SiteRepository
from app.repositories.user import UserRepository
from app.repositories.opportunity import OpportunityRepository, OwnershipRepository
from app.schemas.assignment import AssignmentCreate
from app.models.opportunity import OpportunityStatus
from app.services.audit import AuditService
from app.services.lifecycle_automation import LifecycleAutomation


class AssignmentService:
    def __init__(self):
        self.repo = AssignmentRepository()
        self.site_repo = SiteRepository()
        self.user_repo = UserRepository()
        self.opportunity_repo = OpportunityRepository()
        self.ownership_repo = OwnershipRepository()
        self.audit = AuditService()
        self.lifecycle = LifecycleAutomation()

    def create_assignment(self, db: Session, user: User, data: AssignmentCreate):
        if user.role not in (Role.MANAGER, Role.ADMINISTRATOR):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manager access required")
        if not self.site_repo.get(db, str(data.site_id)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")
        if not self.user_repo.get(db, str(data.assigned_to)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignee not found")

        assignment_data = data.model_dump()
        assignment_data["assigned_by"] = user.id
        assignment_data["assigned_at"] = datetime.now(timezone.utc)
        assignment = self.repo.create(db, assignment_data)

        opportunities = self.opportunity_repo.get_by_site(db, data.site_id)
        if opportunities:
            ownership = self.ownership_repo.get_by_opportunity(db, opportunities[0].id)
            if ownership:
                owner_update = {}
                if data.assignment_type == "marketing":
                    owner_update["marketing_owner_id"] = data.assigned_to
                elif data.assignment_type == "sales":
                    owner_update["sales_owner_id"] = data.assigned_to
                if owner_update:
                    self.ownership_repo.update(db, ownership, owner_update)

        if data.assignment_type == "marketing":
            self.lifecycle.advance_to(
                db, data.site_id, OpportunityStatus.RELATIONSHIP_BUILDING.value, user,
                "Auto: site assigned to marketing",
            )

        self.audit.log(db, user_id=user.id, entity_type="assignment", entity_id=assignment.id, action="create", new_value=assignment_data)
        return assignment

    def list_assignments(self, db: Session, user: User, skip: int = 0, limit: int = 100):
        if user.role in (Role.MANAGER, Role.CEO, Role.ADMINISTRATOR):
            return self.repo.get_multi(db, skip, limit)
        return self.repo.get_by_assignee(db, user.id, skip, limit)
