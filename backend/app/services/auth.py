from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from sqlalchemy.orm import Session
from app.config import settings
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate

class AuthService:
    """
    Service for authentication operations.
    """
    
    def __init__(self):
        self.user_repository = UserRepository()
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        """
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )

    def get_password_hash(self, password: str) -> str:
        """
        Hash a password.
        """
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    def create_access_token(self, data: dict) -> str:
        """
        Create a JWT access token.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
        return encoded_jwt
    
    def decode_access_token(self, token: str) -> Optional[dict]:
        """
        Decode a JWT access token.
        """
        try:
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            return payload
        except JWTError:
            return None
    
    def authenticate_user(self, db: Session, mobile_number: str, password: str) -> Optional[User]:
        """
        Authenticate a user by mobile number and password.
        """
        user = self.user_repository.get_by_mobile_number(db, mobile_number)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user
    
    def create_user(self, db: Session, user_in: UserCreate) -> User:
        """
        Create a new user with hashed password.
        """
        user_data = user_in.model_dump()
        user_data["hashed_password"] = self.get_password_hash(user_data.pop("password"))
        return self.user_repository.create(db, user_data)
