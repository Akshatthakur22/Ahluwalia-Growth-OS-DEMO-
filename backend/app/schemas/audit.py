from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class AuditLogResponse(BaseModel):
    id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    entity_type: str
    entity_id: uuid.UUID
    action: str
    previous_value: Optional[str] = None
    new_value: Optional[str] = None
    ip_address: Optional[str] = None
    device_information: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
