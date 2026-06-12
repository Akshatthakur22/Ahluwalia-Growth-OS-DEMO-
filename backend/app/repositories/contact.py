from typing import List
from sqlalchemy.orm import Session
from app.models.contact import Contact
from app.repositories.base import BaseRepository


class ContactRepository(BaseRepository[Contact]):
    def __init__(self):
        super().__init__(Contact)

    def get_by_mobile(self, db: Session, mobile_number: str) -> List[Contact]:
        return db.query(Contact).filter(Contact.mobile_number == mobile_number).all()

    def search_by_name(self, db: Session, name: str, skip: int = 0, limit: int = 50) -> List[Contact]:
        return (
            db.query(Contact)
            .filter(Contact.name.ilike(f"%{name}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_site(self, db: Session, site_id) -> List[Contact]:
        return db.query(Contact).filter(Contact.site_id == site_id).all()
