from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
import uuid


class OpportunityCreate(BaseModel):
    site_id: uuid.UUID
    opportunity_name: str
    expected_revenue: Optional[Decimal] = None
    quotation_value: Optional[Decimal] = None
    probability_of_conversion: Optional[Decimal] = None
    follow_up_date: Optional[datetime] = None
    remarks: Optional[str] = None


class OpportunityUpdate(BaseModel):
    opportunity_name: Optional[str] = None
    expected_revenue: Optional[Decimal] = None
    quotation_value: Optional[Decimal] = None
    probability_of_conversion: Optional[Decimal] = None
    follow_up_date: Optional[datetime] = None
    remarks: Optional[str] = None


class OpportunityTransition(BaseModel):
    new_status: str
    remarks: Optional[str] = None


class OpportunityResponse(BaseModel):
    id: uuid.UUID
    site_id: uuid.UUID
    opportunity_name: str
    expected_revenue: Optional[Decimal] = None
    quotation_value: Optional[Decimal] = None
    probability_of_conversion: Optional[Decimal] = None
    current_status: str
    follow_up_date: Optional[datetime] = None
    remarks: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LifecycleHistoryResponse(BaseModel):
    id: uuid.UUID
    opportunity_id: uuid.UUID
    previous_status: Optional[str] = None
    new_status: str
    changed_by: Optional[uuid.UUID] = None
    changed_at: datetime
    remarks: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TransitionResponse(BaseModel):
    previous_status: str
    new_status: str
    transition_timestamp: datetime


class LeadTransferRequest(BaseModel):
    builder_name: Optional[str] = None
    architect_name: Optional[str] = None
    expected_visit_date: datetime
    expected_quantity: Optional[Decimal] = None
    priority: Optional[str] = "high"
    remarks: Optional[str] = None
