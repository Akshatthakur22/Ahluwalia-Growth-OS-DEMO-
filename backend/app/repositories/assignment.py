from typing import List
from sqlalchemy.orm import Session
from app.models.assignment import Assignment
from app.repositories.base import BaseRepository


class AssignmentRepository(BaseRepository[Assignment]):
    def __init__(self):
        super().__init__(Assignment)

    def get_by_assignee(self, db: Session, user_id, skip: int = 0, limit: int = 100) -> List[Assignment]:
        return (
            db.query(Assignment)
            .filter(Assignment.assigned_to == user_id)
            .order_by(Assignment.assigned_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
