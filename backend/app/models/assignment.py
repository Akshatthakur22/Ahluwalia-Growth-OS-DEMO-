from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel
import enum


class AssignmentType(str, enum.Enum):
    MARKETING = "marketing"
    SALES = "sales"


class Assignment(BaseModel):
    """
    Assignment model for tracking responsibility allocation.
    """
    __tablename__ = "assignments"
    
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False, index=True)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=False, index=True)
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    assignment_type = Column(String(50), nullable=False)
    assigned_at = Column(DateTime(timezone=True), nullable=False)
    priority = Column(String(50), nullable=True)
    target_follow_up_date = Column(DateTime(timezone=True), nullable=True)
    remarks = Column(String(1000), nullable=True)
