from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid


class CheckInRequest(BaseModel):
    latitude: str
    longitude: str
    device_information: Optional[str] = None


class CheckOutRequest(BaseModel):
    latitude: str
    longitude: str
    route_summary: Optional[str] = None
    device_information: Optional[str] = None


class CheckInResponse(BaseModel):
    attendance_status: str
    check_in_time: datetime
    id: uuid.UUID

    class Config:
        from_attributes = True


class AttendanceResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    check_in_time: datetime
    check_out_time: Optional[datetime] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    mock_location_detected: bool
    route_summary: Optional[str] = None
    device_information: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TeamAttendanceResponse(AttendanceResponse):
    employee_name: Optional[str] = None
    employee_code: Optional[str] = None
    role: Optional[str] = None


class TodayStatusResponse(BaseModel):
    checked_in: bool
    checked_out: bool
    record: Optional[AttendanceResponse] = None


class AttendanceSummaryResponse(BaseModel):
    checked_in_today: bool
    checked_out_today: bool
    month_check_ins: int
    month_on_time: int
    month_route_logs: int
    avg_hours_in_field: float
    total_records: int


class TeamAttendanceSummaryResponse(BaseModel):
    checked_in_today: int
    total_field_staff: int
    not_checked_in: int
    mock_gps_today: int
    on_route_today: int


class AttendancePageDataResponse(BaseModel):
    today: TodayStatusResponse
    summary: AttendanceSummaryResponse
    records: List[AttendanceResponse]


class TeamAttendancePageDataResponse(BaseModel):
    summary: TeamAttendanceSummaryResponse
    today_records: List[TeamAttendanceResponse]
