from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.contact import ContactRepository
from app.repositories.site import SiteRepository
from app.schemas.contact import ContactCreate, ContactUpdate
from app.services.audit import AuditService


class ContactService:
    def __init__(self):
        self.repo = ContactRepository()
        self.site_repo = SiteRepository()
        self.audit = AuditService()

    def create_contact(self, db: Session, user: User, data: ContactCreate):
        if not self.site_repo.get(db, str(data.site_id)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")
        contact = self.repo.create(db, data.model_dump())
        self.audit.log(db, user_id=user.id, entity_type="contact", entity_id=contact.id, action="create", new_value=data.model_dump())
        return contact

    def list_contacts(self, db: Session, skip: int = 0, limit: int = 100, site_id: str = None):
        if site_id:
            return self.repo.get_by_site(db, site_id)
        return self.repo.get_multi(db, skip, limit)

    def get_contact(self, db: Session, contact_id: str):
        contact = self.repo.get(db, contact_id)
        if not contact:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
        return contact

    def update_contact(self, db: Session, user: User, contact_id: str, data: ContactUpdate):
        contact = self.get_contact(db, contact_id)
        update_data = data.model_dump(exclude_unset=True)
        updated = self.repo.update(db, contact, update_data)
        self.audit.log(db, user_id=user.id, entity_type="contact", entity_id=contact.id, action="update", new_value=update_data)
        return updated
