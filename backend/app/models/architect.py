from sqlalchemy import Column, String, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel


class ArchitectProfile(BaseModel):
    """
    Architect profile model for architect intelligence.
    """
    __tablename__ = "architect_profiles"
    
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    influence_score = Column(Numeric(5, 2), nullable=True)
    loyalty_score = Column(Numeric(5, 2), nullable=True)
    project_potential_score = Column(Numeric(5, 2), nullable=True)
    preferences = Column(String(1000), nullable=True)
    revenue_contribution = Column(Numeric(15, 2), nullable=True)
