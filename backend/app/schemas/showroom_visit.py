from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
import uuid


class ShowroomVisitCreate(BaseModel):
    site_id: uuid.UUID
    visit_date: datetime
    client_name: Optional[str] = None
    client_mobile: Optional[str] = None
    client_address: Optional[str] = None
    client_area: Optional[str] = None
    client_city: Optional[str] = None
    project_type: Optional[str] = None
    project_size: Optional[Decimal] = None
    architect_name: Optional[str] = None
    builder_name: Optional[str] = None
    selected_material: Optional[str] = None
    estimated_quantity: Optional[Decimal] = None
    lead_temperature: Optional[str] = None
    lead_source: Optional[str] = None
    referral_name: Optional[str] = None
    referral_contact: Optional[str] = None
    time_spent_minutes: Optional[int] = None
    presentation_shared: Optional[bool] = False
    video_3d_shared: Optional[bool] = False
    quotation_required: bool = False
    expected_purchase_date: Optional[datetime] = None
    follow_up_date: Optional[datetime] = None
    remarks: Optional[str] = None


class ShowroomVisitUpdate(BaseModel):
    visit_date: Optional[datetime] = None
    client_name: Optional[str] = None
    client_mobile: Optional[str] = None
    selected_material: Optional[str] = None
    estimated_quantity: Optional[Decimal] = None
    lead_temperature: Optional[str] = None
    quotation_required: Optional[bool] = None
    expected_purchase_date: Optional[datetime] = None
    follow_up_date: Optional[datetime] = None
    remarks: Optional[str] = None


class ShowroomVisitResponse(BaseModel):
    id: uuid.UUID
    site_id: uuid.UUID
    sales_executive_id: Optional[uuid.UUID] = None
    visit_date: datetime
    client_name: Optional[str] = None
    client_mobile: Optional[str] = None
    client_address: Optional[str] = None
    client_area: Optional[str] = None
    client_city: Optional[str] = None
    project_type: Optional[str] = None
    project_size: Optional[Decimal] = None
    architect_name: Optional[str] = None
    builder_name: Optional[str] = None
    selected_material: Optional[str] = None
    estimated_quantity: Optional[Decimal] = None
    lead_temperature: Optional[str] = None
    lead_source: Optional[str] = None
    referral_name: Optional[str] = None
    referral_contact: Optional[str] = None
    time_spent_minutes: Optional[int] = None
    presentation_shared: Optional[bool] = None
    video_3d_shared: Optional[bool] = None
    quotation_required: bool
    expected_purchase_date: Optional[datetime] = None
    follow_up_date: Optional[datetime] = None
    remarks: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
