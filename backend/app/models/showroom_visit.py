from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel


class ShowroomVisit(BaseModel):
    __tablename__ = "showroom_visits"

    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False, index=True)
    sales_executive_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    visit_date = Column(DateTime(timezone=True), nullable=False)
    client_name = Column(String(200), nullable=True)
    client_mobile = Column(String(20), nullable=True)
    client_address = Column(String(500), nullable=True)
    client_area = Column(String(100), nullable=True)
    client_city = Column(String(100), nullable=True)
    project_type = Column(String(50), nullable=True)
    project_size = Column(Numeric(15, 2), nullable=True)
    architect_name = Column(String(200), nullable=True)
    builder_name = Column(String(200), nullable=True)
    selected_material = Column(String(500), nullable=True)
    estimated_quantity = Column(Numeric(15, 2), nullable=True)
    lead_temperature = Column(String(20), nullable=True)
    lead_source = Column(String(50), nullable=True)
    referral_name = Column(String(200), nullable=True)
    referral_contact = Column(String(20), nullable=True)
    time_spent_minutes = Column(Integer, nullable=True)
    presentation_shared = Column(Boolean, default=False, nullable=True)
    video_3d_shared = Column(Boolean, default=False, nullable=True)
    quotation_required = Column(Boolean, default=False, nullable=False)
    expected_purchase_date = Column(DateTime(timezone=True), nullable=True)
    follow_up_date = Column(DateTime(timezone=True), nullable=True)
    remarks = Column(String(1000), nullable=True)
