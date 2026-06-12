from sqlalchemy import Column, String, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel
import enum


class SiteStage(str, enum.Enum):
    PLANNING = "planning"
    FOUNDATION = "foundation"
    STRUCTURE = "structure"
    FINISHING = "finishing"
    COMPLETED = "completed"


class ProjectType(str, enum.Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    MIXED_USE = "mixed_use"


class Site(BaseModel):
    """
    Site model representing construction sites discovered by field teams.
    """
    __tablename__ = "sites"
    
    site_name = Column(String(200), nullable=False)
    address = Column(String(500), nullable=False)
    area = Column(String(100), nullable=True)
    city = Column(String(100), nullable=False, index=True)
    latitude = Column(String(50), nullable=True)
    longitude = Column(String(50), nullable=True)
    site_stage = Column(String(50), nullable=True)
    project_type = Column(String(50), nullable=True)
    project_size = Column(Numeric(15, 2), nullable=True)
    estimated_requirement = Column(String(500), nullable=True)
    competitor_brand = Column(String(200), nullable=True)
    competitor_quantity = Column(String(200), nullable=True)
    site_remarks = Column(String(1000), nullable=True)
    decision_maker = Column(String(200), nullable=True)
    expected_purchase_timeline = Column(String(200), nullable=True)
    discovered_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
