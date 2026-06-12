from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel
import enum


class ContactType(str, enum.Enum):
    OWNER = "owner"
    BUILDER = "builder"
    ARCHITECT = "architect"
    REFERRAL = "referral"


class Contact(BaseModel):
    """
    Contact model for stakeholders associated with sites.
    """
    __tablename__ = "contacts"
    
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    contact_type = Column(String(50), nullable=False)
    mobile_number = Column(String(20), nullable=False, index=True)
    alternate_number = Column(String(20), nullable=True)
    address = Column(String(500), nullable=True)
    firm_name = Column(String(200), nullable=True)
    designation = Column(String(100), nullable=True)
    category = Column(String(10), nullable=True)
    remarks = Column(String(1000), nullable=True)
