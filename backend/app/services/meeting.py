from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User, Role
from app.repositories.meeting import MeetingRepository
from app.repositories.site import SiteRepository
from app.repositories.contact import ContactRepository
from app.schemas.meeting import MeetingCreate, MeetingUpdate
from app.models.opportunity import OpportunityStatus
from app.services.audit import AuditService
from app.services.lifecycle_automation import LifecycleAutomation


class MeetingService:
    def __init__(self):
        self.repo = MeetingRepository()
        self.site_repo = SiteRepository()
        self.contact_repo = ContactRepository()
        self.audit = AuditService()
        self.lifecycle = LifecycleAutomation()

    def _sync_meeting_contact(self, db: Session, site_id, data: MeetingCreate):
        if not data.met_with or not data.stakeholder_name or not data.stakeholder_mobile:
            return
        payload = {
            "name": data.stakeholder_name,
            "mobile_number": data.stakeholder_mobile,
            "contact_type": data.met_with,
            "firm_name": data.firm_name,
            "address": data.address,
            "category": data.category,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        existing = self.contact_repo.get_by_site_and_type(db, site_id, data.met_with)
        if existing:
            self.contact_repo.update(db, existing, payload)
        else:
            self.contact_repo.create(db, {"site_id": site_id, **payload})

    def create_meeting(self, db: Session, user: User, data: MeetingCreate):
        if not self.site_repo.get(db, str(data.site_id)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")
        meeting_data = data.model_dump()
        meeting_data["conducted_by"] = user.id
        meeting = self.repo.create(db, meeting_data)
        self._sync_meeting_contact(db, data.site_id, data)
        self.audit.log(db, user_id=user.id, entity_type="meeting", entity_id=meeting.id, action="create", new_value=meeting_data)
        self.lifecycle.advance_to(
            db, data.site_id, OpportunityStatus.RELATIONSHIP_BUILDING.value, user,
            "Auto: marketing meeting recorded",
        )
        if data.showroom_visit_commitment:
            self.lifecycle.advance_to(
                db, data.site_id, OpportunityStatus.SHOWROOM_VISIT_SCHEDULED.value, user,
                "Auto: showroom visit commitment from meeting",
            )
        return meeting

    def list_meetings(self, db: Session, user: User, skip: int = 0, limit: int = 100):
        if user.role in (Role.MANAGER, Role.CEO, Role.ADMINISTRATOR):
            return self.repo.get_multi(db, skip, limit)
        if user.role == Role.MARKETING_EXECUTIVE:
            return self.repo.get_by_conductor(db, user.id, skip, limit)
        return self.repo.get_multi(db, skip, limit)

    def get_meeting(self, db: Session, meeting_id: str):
        meeting = self.repo.get(db, meeting_id)
        if not meeting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
        return meeting

    def update_meeting(self, db: Session, user: User, meeting_id: str, data: MeetingUpdate):
        meeting = self.get_meeting(db, meeting_id)
        update_data = data.model_dump(exclude_unset=True)
        updated = self.repo.update(db, meeting, update_data)
        self.audit.log(db, user_id=user.id, entity_type="meeting", entity_id=meeting.id, action="update", new_value=update_data)
        return updated
