from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, EmploymentStatus
from app.services.auth import AuthService

security = HTTPBearer()
auth_service = AuthService()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = auth_service.decode_access_token(token)
    
    if payload is None:
        raise credentials_exception
    
    mobile_number: str = payload.get("sub")
    if mobile_number is None:
        raise credentials_exception
    
    user = auth_service.user_repository.get_by_mobile_number(db, mobile_number)
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get the current active user.
    """
    if current_user.status != EmploymentStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
