from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, Role
from app.repositories.showroom_visit import ShowroomVisitRepository
from app.repositories.site import SiteRepository
from app.schemas.showroom_visit import ShowroomVisitCreate, ShowroomVisitUpdate
from app.models.opportunity import OpportunityStatus
from app.services.audit import AuditService
from app.services.lifecycle_automation import LifecycleAutomation


class ShowroomVisitService:
    def __init__(self):
        self.repo = ShowroomVisitRepository()
        self.site_repo = SiteRepository()
        self.audit = AuditService()
        self.lifecycle = LifecycleAutomation()

    def create_visit(self, db: Session, user: User, data: ShowroomVisitCreate):
        if not self.site_repo.get(db, str(data.site_id)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")
        visit_data = data.model_dump()
        visit_data["sales_executive_id"] = user.id
        visit = self.repo.create(db, visit_data)
        self.audit.log(db, user_id=user.id, entity_type="showroom_visit", entity_id=visit.id, action="create", new_value=visit_data)
        self.lifecycle.advance_to(
            db, data.site_id, OpportunityStatus.SHOWROOM_VISIT_DONE.value, user,
            "Auto: showroom visit logged",
        )
        if data.quotation_required:
            self.lifecycle.advance_to(
                db, data.site_id, OpportunityStatus.SELECTION_DONE.value, user,
                "Auto: material selected, quotation requested",
            )
        return visit

    def list_visits(self, db: Session, user: User, skip: int = 0, limit: int = 100):
        if user.role in (Role.MANAGER, Role.CEO, Role.ADMINISTRATOR):
            return self.repo.get_multi(db, skip, limit)
        if user.role == Role.SALES_EXECUTIVE:
            return self.repo.get_by_sales_exec(db, user.id, skip, limit)
        return self.repo.get_multi(db, skip, limit)

    def get_visit(self, db: Session, visit_id: str):
        visit = self.repo.get(db, visit_id)
        if not visit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Showroom visit not found")
        return visit

    def update_visit(self, db: Session, user: User, visit_id: str, data: ShowroomVisitUpdate):
        visit = self.get_visit(db, visit_id)
        update_data = data.model_dump(exclude_unset=True)
        updated = self.repo.update(db, visit, update_data)
        self.audit.log(db, user_id=user.id, entity_type="showroom_visit", entity_id=visit.id, action="update", new_value=update_data)
        return updated
