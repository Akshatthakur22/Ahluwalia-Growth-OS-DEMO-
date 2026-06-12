from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate, AssignableUserResponse
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.api.deps import get_current_active_user
from app.models.user import User, Role

router = APIRouter()
user_repository = UserRepository()
auth_service = AuthService()


def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Require administrator role.
    """
    if current_user.role != Role.ADMINISTRATOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required"
        )
    return current_user


@router.post("/", response_model=UserResponse, dependencies=[Depends(require_admin)])
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user (admin only).
    """
    # Check if mobile number already exists
    existing_user = user_repository.get_by_mobile_number(db, user_in.mobile_number)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mobile number already registered"
        )
    
    # Check if employee code already exists
    existing_code = user_repository.get_by_employee_code(db, user_in.employee_code)
    if existing_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee code already exists"
        )
    
    # Check if email already exists
    if user_in.email:
        existing_email = user_repository.get_by_email(db, user_in.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    user = auth_service.create_user(db, user_in)
    return UserResponse.model_validate(user)


@router.get("/assignable", response_model=List[AssignableUserResponse])
def list_assignable_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    List users that managers can assign opportunities to (demo + assignment flow).
    """
    if current_user.role not in (Role.MANAGER, Role.ADMINISTRATOR):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager access required",
        )
    assignable_roles = (
        Role.MARKETING_EXECUTIVE,
        Role.SALES_EXECUTIVE,
        Role.FIELD_EXECUTIVE,
    )
    users = (
        db.query(User)
        .filter(User.role.in_(assignable_roles))
        .order_by(User.full_name)
        .all()
    )
    return [AssignableUserResponse.model_validate(u) for u in users]


@router.get("/", response_model=List[UserResponse], dependencies=[Depends(require_admin)])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all users (admin only).
    """
    users = user_repository.get_multi(db, skip=skip, limit=limit)
    return [UserResponse.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get user by ID.
    - Admins can view any user
    - Other users can only view themselves
    """
    if current_user.role != Role.ADMINISTRATOR and str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this user"
        )
    
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.model_validate(user)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update user.
    - Admins can update any user
    - Other users can only update themselves
    - Role changes require admin access
    """
    if current_user.role != Role.ADMINISTRATOR and str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )
    
    # Non-admins cannot change role or status
    if current_user.role != Role.ADMINISTRATOR:
        if user_in.role is not None or user_in.status is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to change role or status"
            )
    
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Filter out None values
    update_data = user_in.model_dump(exclude_unset=True)
    updated_user = user_repository.update(db, user, update_data)
    
    return UserResponse.model_validate(updated_user)
