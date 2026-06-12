from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.user import User, Role
from app.repositories.attendance import AttendanceRepository
from app.schemas.attendance import CheckInRequest, CheckOutRequest
from app.services.audit import AuditService

# Ahluwalia operating region (NCR / North India demo bounds)
REGION_LAT_MIN, REGION_LAT_MAX = 27.5, 30.5
REGION_LON_MIN, REGION_LON_MAX = 76.0, 78.5

# Known spoofed coordinates from demo / common mock apps
KNOWN_MOCK_COORDS = [
    (0.0, 0.0),
    (19.0760, 72.8777),  # Mumbai — used in demo seed for mock incident
    (37.4220, -122.0841),  # Google HQ default emulator
]


class AttendanceService:
    def __init__(self):
        self.repo = AttendanceRepository()
        self.audit = AuditService()

    def _parse_coords(self, latitude: str, longitude: str) -> tuple[float, float]:
        try:
            return float(latitude), float(longitude)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid GPS coordinates. Enable location services and try again.",
            )

    def _is_mock_location(self, latitude: str, longitude: str) -> bool:
        lat, lon = self._parse_coords(latitude, longitude)
        for mock_lat, mock_lon in KNOWN_MOCK_COORDS:
            if abs(lat - mock_lat) < 0.0001 and abs(lon - mock_lon) < 0.0001:
                return True
        if not (REGION_LAT_MIN <= lat <= REGION_LAT_MAX and REGION_LON_MIN <= lon <= REGION_LON_MAX):
            return True
        return False

    def check_in(self, db: Session, user: User, data: CheckInRequest):
        if self._is_mock_location(data.latitude, data.longitude):
            self.audit.log(
                db,
                user_id=user.id,
                entity_type="attendance",
                entity_id=user.id,
                action="check_in_blocked",
                new_value={"reason": "mock_gps", "latitude": data.latitude, "longitude": data.longitude},
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mock or invalid GPS location detected. Attendance cannot be recorded. Disable fake GPS apps and try again.",
            )

        existing = self.repo.get_today_checkin(db, user.id)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already checked in today")

        record = self.repo.create(db, {
            "user_id": user.id,
            "check_in_time": datetime.now(timezone.utc),
            "latitude": data.latitude,
            "longitude": data.longitude,
            "mock_location_detected": False,
            "device_information": data.device_information,
        })
        self.audit.log(
            db,
            user_id=user.id,
            entity_type="attendance",
            entity_id=record.id,
            action="check_in",
            new_value={"latitude": data.latitude, "longitude": data.longitude},
        )
        return record

    def check_out(self, db: Session, user: User, data: CheckOutRequest):
        if self._is_mock_location(data.latitude, data.longitude):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mock or invalid GPS location detected. Check-out cannot be recorded.",
            )

        record = self.repo.get_today_checkin(db, user.id)
        if not record:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No check-in found for today")
        if record.check_out_time:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already checked out today")

        route = data.route_summary.strip() if data.route_summary else (record.route_summary or "Field day completed")
        updated = self.repo.update(db, record, {
            "check_out_time": datetime.now(timezone.utc),
            "route_summary": route,
        })
        self.audit.log(
            db,
            user_id=user.id,
            entity_type="attendance",
            entity_id=updated.id,
            action="check_out",
            new_value={"route_summary": route},
        )
        return updated

    def get_today_status(self, db: Session, user: User) -> dict:
        record = self.repo.get_today_checkin(db, user.id)
        if not record:
            return {"checked_in": False, "checked_out": False, "record": None}
        return {
            "checked_in": True,
            "checked_out": record.check_out_time is not None,
            "record": record,
        }

    _MONTH_STATS_SQL = text("""
        SELECT
          COUNT(*) FILTER (WHERE check_in_time >= :month_start)::int AS month_check_ins,
          COUNT(*) FILTER (WHERE check_in_time >= :month_start AND (
            EXTRACT(HOUR FROM check_in_time) < 10 OR
            (EXTRACT(HOUR FROM check_in_time) = 10 AND EXTRACT(MINUTE FROM check_in_time) <= 30)
          ))::int AS month_on_time,
          COUNT(*) FILTER (WHERE check_in_time >= :month_start AND route_summary IS NOT NULL AND route_summary != '')::int AS month_route_logs,
          COALESCE(AVG(
            EXTRACT(EPOCH FROM (check_out_time - check_in_time)) / 3600
          ) FILTER (WHERE check_in_time >= :month_start AND check_out_time IS NOT NULL), 0) AS avg_hours,
          COUNT(*)::int AS total_records
        FROM attendance_logs
        WHERE user_id = :uid
    """)

    def _month_stats(self, db: Session, user: User) -> dict:
        today = datetime.now(timezone.utc).date()
        month_start = datetime(today.year, today.month, 1, tzinfo=timezone.utc)
        row = db.execute(
            self._MONTH_STATS_SQL,
            {"uid": user.id, "month_start": month_start},
        ).mappings().one()
        return {
            "month_check_ins": int(row["month_check_ins"] or 0),
            "month_on_time": int(row["month_on_time"] or 0),
            "month_route_logs": int(row["month_route_logs"] or 0),
            "avg_hours_in_field": round(float(row["avg_hours"] or 0), 1),
            "total_records": int(row["total_records"] or 0),
        }

    def get_my_summary(self, db: Session, user: User) -> dict:
        today_record = self.repo.get_today_checkin(db, user.id)
        stats = self._month_stats(db, user)
        return {
            **stats,
            "checked_in_today": today_record is not None,
            "checked_out_today": today_record is not None and today_record.check_out_time is not None,
        }

    def get_my_page_data(self, db: Session, user: User, skip: int = 0, limit: int = 30) -> dict:
        today_record = self.repo.get_today_checkin(db, user.id)
        today = {
            "checked_in": today_record is not None,
            "checked_out": today_record is not None and today_record.check_out_time is not None,
            "record": today_record,
        }
        stats = self._month_stats(db, user)
        summary = {
            **stats,
            "checked_in_today": today["checked_in"],
            "checked_out_today": today["checked_out"],
        }
        records = self.repo.get_by_user(db, user.id, skip, min(limit, 50))
        return {"today": today, "summary": summary, "records": records}

    def get_my_attendance(self, db: Session, user: User, skip: int = 0, limit: int = 100):
        return self.repo.get_by_user(db, user.id, skip, limit)

    def get_team_attendance(self, db: Session, user: User, skip: int = 0, limit: int = 100):
        if user.role not in (Role.MANAGER, Role.CEO, Role.ADMINISTRATOR):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manager access required")
        return self.repo.get_team_attendance_with_users(db, skip, limit)

    _TEAM_SUMMARY_SQL = text("""
        SELECT
          (SELECT COUNT(*)::int FROM users
           WHERE status::text IN ('active', 'ACTIVE')
           AND role::text IN ('FIELD_EXECUTIVE', 'MARKETING_EXECUTIVE', 'SALES_EXECUTIVE')
          ) AS total_field_staff,
          COUNT(DISTINCT user_id)::int AS checked_in_today,
          COUNT(*) FILTER (WHERE mock_location_detected = true)::int AS mock_gps_today,
          COUNT(*) FILTER (WHERE route_summary IS NOT NULL AND route_summary != '')::int AS on_route_today
        FROM attendance_logs
        WHERE check_in_time >= :today_start
    """)

    def get_team_page_data(self, db: Session, user: User) -> dict:
        if user.role not in (Role.MANAGER, Role.CEO, Role.ADMINISTRATOR):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manager access required")
        today_start = datetime.combine(
            datetime.now(timezone.utc).date(), datetime.min.time()
        ).replace(tzinfo=timezone.utc)
        summary = self.get_team_summary(db, user)
        today_rows = self.repo.get_team_attendance_with_users(db, 0, 100, since=today_start)
        return {"summary": summary, "today_records": today_rows}

    def get_team_summary(self, db: Session, user: User) -> dict:
        if user.role not in (Role.MANAGER, Role.CEO, Role.ADMINISTRATOR):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manager access required")

        today_start = datetime.combine(
            datetime.now(timezone.utc).date(), datetime.min.time()
        ).replace(tzinfo=timezone.utc)

        row = db.execute(self._TEAM_SUMMARY_SQL, {"today_start": today_start}).mappings().one()
        total_field = int(row["total_field_staff"] or 0)
        checked_in = int(row["checked_in_today"] or 0)

        return {
            "checked_in_today": checked_in,
            "total_field_staff": total_field,
            "not_checked_in": max(0, total_field - checked_in),
            "mock_gps_today": int(row["mock_gps_today"] or 0),
            "on_route_today": int(row["on_route_today"] or 0),
        }
