from typing import List
from sqlalchemy.orm import Session
from app.models.meeting import Meeting
from app.repositories.base import BaseRepository


class MeetingRepository(BaseRepository[Meeting]):
    def __init__(self):
        super().__init__(Meeting)

    def get_by_conductor(self, db: Session, user_id, skip: int = 0, limit: int = 100) -> List[Meeting]:
        return (
            db.query(Meeting)
            .filter(Meeting.conducted_by == user_id)
            .order_by(Meeting.meeting_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
