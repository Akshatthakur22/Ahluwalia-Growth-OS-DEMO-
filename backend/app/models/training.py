from sqlalchemy import Column, String, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel
import enum


class CompletionStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class CertificationStatus(str, enum.Enum):
    NOT_CERTIFIED = "not_certified"
    CERTIFIED = "certified"
    EXPIRED = "expired"


class TrainingProgram(BaseModel):
    """
    Training program model for LMS.
    """
    __tablename__ = "training_programs"
    
    title = Column(String(200), nullable=False)
    description = Column(String(2000), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)


class TrainingProgress(BaseModel):
    """
    Training progress model for tracking employee learning.
    """
    __tablename__ = "training_progress"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    training_program_id = Column(UUID(as_uuid=True), ForeignKey("training_programs.id", ondelete="CASCADE"), nullable=False, index=True)
    completion_status = Column(String(50), nullable=False, default=CompletionStatus.NOT_STARTED)
    assessment_score = Column(Numeric(5, 2), nullable=True)
    certification_status = Column(String(50), nullable=False, default=CertificationStatus.NOT_CERTIFIED)
