from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.opportunity import Opportunity
from app.models.lifecycle import LifecycleHistory
from app.models.ownership import OwnershipRecord
from app.repositories.base import BaseRepository


class OpportunityRepository(BaseRepository[Opportunity]):
    def __init__(self):
        super().__init__(Opportunity)

    def get_by_site(self, db: Session, site_id) -> List[Opportunity]:
        return db.query(Opportunity).filter(Opportunity.site_id == site_id).all()

    def count_by_status(self, db: Session) -> Dict[str, int]:
        rows = (
            db.query(Opportunity.current_status, func.count(Opportunity.id))
            .group_by(Opportunity.current_status)
            .all()
        )
        return {status: count for status, count in rows}

    def get_by_sites(self, db: Session, site_ids: List) -> List[Opportunity]:
        if not site_ids:
            return []
        return db.query(Opportunity).filter(Opportunity.site_id.in_(site_ids)).all()


class LifecycleRepository(BaseRepository[LifecycleHistory]):
    def __init__(self):
        super().__init__(LifecycleHistory)

    def get_by_opportunity(self, db: Session, opportunity_id) -> List[LifecycleHistory]:
        return (
            db.query(LifecycleHistory)
            .filter(LifecycleHistory.opportunity_id == opportunity_id)
            .order_by(LifecycleHistory.changed_at.desc())
            .all()
        )


class OwnershipRepository(BaseRepository[OwnershipRecord]):
    def __init__(self):
        super().__init__(OwnershipRecord)

    def get_by_opportunity(self, db: Session, opportunity_id) -> Optional[OwnershipRecord]:
        return db.query(OwnershipRecord).filter(OwnershipRecord.opportunity_id == opportunity_id).first()
