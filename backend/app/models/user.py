import uuid
from sqlalchemy import Column, String, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel
import enum


class EmploymentStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"


class Role(str, enum.Enum):
    FIELD_EXECUTIVE = "field_executive"
    MARKETING_EXECUTIVE = "marketing_executive"
    SALES_EXECUTIVE = "sales_executive"
    MANAGER = "manager"
    CEO = "ceo"
    ADMINISTRATOR = "administrator"


class User(BaseModel):
    """
    User model representing employees in the system.
    """
    __tablename__ = "users"
    
    employee_code = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(200), nullable=False)
    mobile_number = Column(String(20), unique=True, nullable=False, index=True)
    email = Column(String(200), unique=True, nullable=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLEnum(Role), nullable=False, default=Role.FIELD_EXECUTIVE)
    department = Column(String(100), nullable=True)
    manager_id = Column(UUID(as_uuid=True), nullable=True)
    status = Column(SQLEnum(EmploymentStatus), nullable=False, default=EmploymentStatus.ACTIVE)
    assigned_region = Column(String(200), nullable=True)
    date_of_joining = Column(String(50), nullable=True)
