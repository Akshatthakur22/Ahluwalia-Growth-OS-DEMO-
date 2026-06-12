from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class ContactCreate(BaseModel):
    site_id: uuid.UUID
    name: str
    contact_type: str
    mobile_number: str
    alternate_number: Optional[str] = None
    address: Optional[str] = None
    firm_name: Optional[str] = None
    designation: Optional[str] = None
    category: Optional[str] = None
    remarks: Optional[str] = None


class ContactUpdate(BaseModel):
    name: Optional[str] = None
    contact_type: Optional[str] = None
    mobile_number: Optional[str] = None
    alternate_number: Optional[str] = None
    address: Optional[str] = None
    firm_name: Optional[str] = None
    designation: Optional[str] = None
    category: Optional[str] = None
    remarks: Optional[str] = None


class ContactResponse(BaseModel):
    id: uuid.UUID
    site_id: uuid.UUID
    name: str
    contact_type: str
    mobile_number: str
    alternate_number: Optional[str] = None
    address: Optional[str] = None
    firm_name: Optional[str] = None
    designation: Optional[str] = None
    category: Optional[str] = None
    remarks: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
