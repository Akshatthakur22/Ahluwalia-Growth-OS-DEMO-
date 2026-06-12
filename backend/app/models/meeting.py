from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Numeric, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel
import enum


class MeetingType(str, enum.Enum):
    SITE_VISIT = "site_visit"
    OFFICE_VISIT = "office_visit"
    PHONE_CALL = "phone_call"
    VIDEO_CALL = "video_call"


class Meeting(BaseModel):
    __tablename__ = "meetings"

    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False, index=True)
    conducted_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    meeting_date = Column(DateTime(timezone=True), nullable=False)
    meeting_type = Column(String(50), nullable=True)
    stakeholder_name = Column(String(200), nullable=False)
    stakeholder_mobile = Column(String(20), nullable=True)
    summary = Column(Text, nullable=True)
    follow_up_date = Column(DateTime(timezone=True), nullable=True)
    relationship_score = Column(String(50), nullable=True)
    influence_score = Column(Numeric(4, 1), nullable=True)
    opportunity_score = Column(Numeric(4, 1), nullable=True)
    loyalty_score = Column(Numeric(4, 1), nullable=True)
    showroom_visit_commitment = Column(Boolean, default=False, nullable=True)
    time_spent_minutes = Column(Integer, nullable=True)
    current_requirement = Column(Text, nullable=True)
    estimated_project_size = Column(Numeric(15, 2), nullable=True)
    latitude = Column(String(50), nullable=True)
    longitude = Column(String(50), nullable=True)
    remarks = Column(String(1000), nullable=True)
