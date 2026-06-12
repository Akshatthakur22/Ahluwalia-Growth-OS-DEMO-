from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from decimal import Decimal
import uuid

from app.schemas.contact import ContactResponse


class SiteBaseFields(BaseModel):
    site_name: str
    address: str
    city: str
    area: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    site_stage: Optional[str] = None
    project_type: Optional[str] = None
    project_size: Optional[Decimal] = None
    estimated_requirement: Optional[str] = None
    current_vendor: Optional[str] = None
    material_used: Optional[str] = None
    purchase_rate: Optional[Decimal] = None
    competitor_brand: Optional[str] = None
    competitor_quantity: Optional[str] = None
    site_remarks: Optional[str] = None
    decision_maker: Optional[str] = None
    expected_purchase_timeline: Optional[str] = None


class StakeholderFields(BaseModel):
    """PDF Field Executive — owner, builder, architect blocks."""
    owner_name: Optional[str] = None
    owner_mobile: Optional[str] = None
    owner_address: Optional[str] = None
    builder_name: Optional[str] = None
    builder_firm_name: Optional[str] = None
    builder_mobile: Optional[str] = None
    builder_category: Optional[str] = None
    architect_name: Optional[str] = None
    architect_firm_name: Optional[str] = None
    architect_mobile: Optional[str] = None
    architect_category: Optional[str] = None


class SiteCaptureCreate(SiteBaseFields, StakeholderFields):
    pass


class SiteCaptureUpdate(BaseModel):
    site_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    area: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    site_stage: Optional[str] = None
    project_type: Optional[str] = None
    project_size: Optional[Decimal] = None
    estimated_requirement: Optional[str] = None
    current_vendor: Optional[str] = None
    material_used: Optional[str] = None
    purchase_rate: Optional[Decimal] = None
    competitor_brand: Optional[str] = None
    competitor_quantity: Optional[str] = None
    site_remarks: Optional[str] = None
    decision_maker: Optional[str] = None
    expected_purchase_timeline: Optional[str] = None
    owner_name: Optional[str] = None
    owner_mobile: Optional[str] = None
    owner_address: Optional[str] = None
    builder_name: Optional[str] = None
    builder_firm_name: Optional[str] = None
    builder_mobile: Optional[str] = None
    builder_category: Optional[str] = None
    architect_name: Optional[str] = None
    architect_firm_name: Optional[str] = None
    architect_mobile: Optional[str] = None
    architect_category: Optional[str] = None


# Legacy aliases
class SiteCreate(SiteCaptureCreate):
    pass


class SiteUpdate(SiteCaptureUpdate):
    pass


class SiteResponse(BaseModel):
    id: uuid.UUID
    site_name: str
    address: str
    area: Optional[str] = None
    city: str
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    site_stage: Optional[str] = None
    project_type: Optional[str] = None
    project_size: Optional[Decimal] = None
    estimated_requirement: Optional[str] = None
    current_vendor: Optional[str] = None
    material_used: Optional[str] = None
    purchase_rate: Optional[Decimal] = None
    competitor_brand: Optional[str] = None
    competitor_quantity: Optional[str] = None
    site_remarks: Optional[str] = None
    decision_maker: Optional[str] = None
    expected_purchase_timeline: Optional[str] = None
    discovered_by: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SiteLookupItem(BaseModel):
    id: uuid.UUID
    site_name: str

    class Config:
        from_attributes = True


class SitePipelineItem(BaseModel):
    id: uuid.UUID
    opportunity_name: str
    current_status: str
    expected_revenue: Optional[Decimal] = None


class SiteWithPipelineResponse(BaseModel):
    sites: List[SiteResponse]
    opportunities_by_site: Dict[str, SitePipelineItem]


class SiteMediaCreate(BaseModel):
    media_type: str = "site_photo"
    file_url: str
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    captured_at: Optional[datetime] = None


class SiteMediaResponse(BaseModel):
    id: uuid.UUID
    site_id: uuid.UUID
    media_type: str
    file_url: str
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    captured_at: Optional[datetime] = None
    uploaded_by: Optional[uuid.UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SiteDetailResponse(SiteResponse):
    contacts: List[ContactResponse] = []
    stakeholders: StakeholderFields = StakeholderFields()
    media: List[SiteMediaResponse] = []
