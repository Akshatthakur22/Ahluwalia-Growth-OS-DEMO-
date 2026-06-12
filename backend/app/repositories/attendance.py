from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.attendance import AttendanceLog
from app.models.user import User
from app.repositories.base import BaseRepository


class AttendanceRepository(BaseRepository[AttendanceLog]):
    def __init__(self):
        super().__init__(AttendanceLog)

    def get_today_checkin(self, db: Session, user_id) -> Optional[AttendanceLog]:
        today = datetime.now(timezone.utc).date()
        return (
            db.query(AttendanceLog)
            .filter(AttendanceLog.user_id == user_id)
            .filter(AttendanceLog.check_in_time >= datetime.combine(today, datetime.min.time()).replace(tzinfo=timezone.utc))
            .first()
        )

    def get_by_user(self, db: Session, user_id, skip: int = 0, limit: int = 100) -> List[AttendanceLog]:
        return (
            db.query(AttendanceLog)
            .filter(AttendanceLog.user_id == user_id)
            .order_by(AttendanceLog.check_in_time.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_team_attendance(self, db: Session, skip: int = 0, limit: int = 100) -> List[AttendanceLog]:
        return (
            db.query(AttendanceLog)
            .order_by(AttendanceLog.check_in_time.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_team_attendance_with_users(
        self, db: Session, skip: int = 0, limit: int = 100, since=None,
    ):
        q = (
            db.query(AttendanceLog, User.full_name, User.employee_code, User.role)
            .join(User, AttendanceLog.user_id == User.id)
        )
        if since is not None:
            q = q.filter(AttendanceLog.check_in_time >= since)
        return (
            q.order_by(AttendanceLog.check_in_time.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
