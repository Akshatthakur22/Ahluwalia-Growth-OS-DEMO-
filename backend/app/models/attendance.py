from sqlalchemy import Column, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel
import uuid


class AttendanceLog(BaseModel):
    """
    Attendance log model for tracking employee check-ins and location.
    """
    __tablename__ = "attendance_logs"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    check_in_time = Column(DateTime(timezone=True), nullable=False)
    check_out_time = Column(DateTime(timezone=True), nullable=True)
    latitude = Column(String(50), nullable=True)
    longitude = Column(String(50), nullable=True)
    mock_location_detected = Column(Boolean, default=False, nullable=False)
    route_summary = Column(Text, nullable=True)
    device_information = Column(String(500), nullable=True)
