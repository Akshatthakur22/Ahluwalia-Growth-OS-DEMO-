from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel
import enum


class OpportunityStatus(str, enum.Enum):
    NEW_SITE = "new_site"
    RELATIONSHIP_BUILDING = "relationship_building"
    SHOWROOM_VISIT_SCHEDULED = "showroom_visit_scheduled"
    SHOWROOM_VISIT_DONE = "showroom_visit_done"
    SELECTION_DONE = "selection_done"
    QUOTATION_SENT = "quotation_sent"
    NEGOTIATION = "negotiation"
    ORDER_CONFIRMED = "order_confirmed"
    LOST = "lost"


class Opportunity(BaseModel):
    """
    Opportunity model for sales opportunities.
    """
    __tablename__ = "opportunities"
    
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False, index=True)
    opportunity_name = Column(String(200), nullable=False)
    expected_revenue = Column(Numeric(15, 2), nullable=True)
    quotation_value = Column(Numeric(15, 2), nullable=True)
    probability_of_conversion = Column(Numeric(5, 2), nullable=True)
    current_status = Column(String(50), nullable=False, default=OpportunityStatus.NEW_SITE, index=True)
    follow_up_date = Column(DateTime(timezone=True), nullable=True)
    remarks = Column(String(1000), nullable=True)
