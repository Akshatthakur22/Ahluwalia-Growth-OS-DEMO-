from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
import uuid


class MeetingCreate(BaseModel):
    site_id: uuid.UUID
    meeting_date: datetime
    meeting_type: Optional[str] = None
    stakeholder_name: str
    stakeholder_mobile: Optional[str] = None
    summary: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    relationship_score: Optional[str] = None
    influence_score: Optional[Decimal] = None
    opportunity_score: Optional[Decimal] = None
    loyalty_score: Optional[Decimal] = None
    showroom_visit_commitment: Optional[bool] = False
    time_spent_minutes: Optional[int] = None
    current_requirement: Optional[str] = None
    estimated_project_size: Optional[Decimal] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    remarks: Optional[str] = None


class MeetingUpdate(BaseModel):
    meeting_date: Optional[datetime] = None
    meeting_type: Optional[str] = None
    stakeholder_name: Optional[str] = None
    stakeholder_mobile: Optional[str] = None
    summary: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    relationship_score: Optional[str] = None
    influence_score: Optional[Decimal] = None
    opportunity_score: Optional[Decimal] = None
    loyalty_score: Optional[Decimal] = None
    showroom_visit_commitment: Optional[bool] = None
    time_spent_minutes: Optional[int] = None
    current_requirement: Optional[str] = None
    estimated_project_size: Optional[Decimal] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    remarks: Optional[str] = None


class MeetingResponse(BaseModel):
    id: uuid.UUID
    site_id: uuid.UUID
    conducted_by: Optional[uuid.UUID] = None
    meeting_date: datetime
    meeting_type: Optional[str] = None
    stakeholder_name: str
    stakeholder_mobile: Optional[str] = None
    summary: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    relationship_score: Optional[str] = None
    influence_score: Optional[Decimal] = None
    opportunity_score: Optional[Decimal] = None
    loyalty_score: Optional[Decimal] = None
    showroom_visit_commitment: Optional[bool] = None
    time_spent_minutes: Optional[int] = None
    current_requirement: Optional[str] = None
    estimated_project_size: Optional[Decimal] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    remarks: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
