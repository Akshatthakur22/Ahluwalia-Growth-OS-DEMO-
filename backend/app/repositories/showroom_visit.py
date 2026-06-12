from typing import List
from sqlalchemy.orm import Session
from app.models.showroom_visit import ShowroomVisit
from app.repositories.base import BaseRepository


class ShowroomVisitRepository(BaseRepository[ShowroomVisit]):
    def __init__(self):
        super().__init__(ShowroomVisit)

    def get_by_sales_exec(self, db: Session, user_id, skip: int = 0, limit: int = 100) -> List[ShowroomVisit]:
        return (
            db.query(ShowroomVisit)
            .filter(ShowroomVisit.sales_executive_id == user_id)
            .order_by(ShowroomVisit.visit_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
