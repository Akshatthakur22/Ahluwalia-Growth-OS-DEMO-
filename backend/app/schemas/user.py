from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid


class UserBase(BaseModel):
    employee_code: str
    full_name: str
    mobile_number: str
    email: Optional[EmailStr] = None
    role: str
    department: Optional[str] = None
    assigned_region: Optional[str] = None
    date_of_joining: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    assigned_region: Optional[str] = None
    status: Optional[str] = None
    role: Optional[str] = None


class UserResponse(UserBase):
    id: uuid.UUID
    manager_id: Optional[uuid.UUID] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    mobile_number: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class AssignableUserResponse(BaseModel):
    id: uuid.UUID
    full_name: str
    role: str

    class Config:
        from_attributes = True
