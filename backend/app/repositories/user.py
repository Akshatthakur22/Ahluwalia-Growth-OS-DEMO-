from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for User model operations.
    """

    def __init__(self):
        super().__init__(User)

    def get_by_mobile_number(self, db: Session, mobile_number: str) -> Optional[User]:
        """
        Get user by mobile number.
        """
        return db.query(User).filter(User.mobile_number == mobile_number).first()
    
    def get_by_employee_code(self, db: Session, employee_code: str) -> Optional[User]:
        """
        Get user by employee code.
        """
        return db.query(User).filter(User.employee_code == employee_code).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        Get user by email.
        """
        return db.query(User).filter(User.email == email).first()
    
    def get_by_role(self, db: Session, role: str, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get users by role.
        """
        return db.query(User).filter(User.role == role).offset(skip).limit(limit).all()
    
    def get_active_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all active users.
        """
        return db.query(User).filter(User.status == "active").offset(skip).limit(limit).all()
