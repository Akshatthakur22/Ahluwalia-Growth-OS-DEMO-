from sqlalchemy import Column, String, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel


class BuilderProfile(BaseModel):
    """
    Builder profile model for builder intelligence.
    """
    __tablename__ = "builder_profiles"
    
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    project_volume = Column(Numeric(15, 2), nullable=True)
    business_potential = Column(String(500), nullable=True)
    consumption_potential = Column(Numeric(15, 2), nullable=True)
    future_requirements = Column(String(1000), nullable=True)
