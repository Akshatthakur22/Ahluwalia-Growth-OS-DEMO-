from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class AssignmentCreate(BaseModel):
    site_id: uuid.UUID
    assigned_to: uuid.UUID
    assignment_type: str
    priority: Optional[str] = None
    target_follow_up_date: Optional[datetime] = None
    remarks: Optional[str] = None


class AssignmentResponse(BaseModel):
    id: uuid.UUID
    site_id: uuid.UUID
    assigned_to: uuid.UUID
    assigned_by: Optional[uuid.UUID] = None
    assignment_type: str
    assigned_at: datetime
    priority: Optional[str] = None
    target_follow_up_date: Optional[datetime] = None
    remarks: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
