from typing import Callable
from fastapi import Depends, HTTPException, status
from app.api.deps import get_current_active_user
from app.models.user import User, Role


def require_roles(*allowed_roles: Role) -> Callable:
    """Dependency factory that restricts access to specific roles (admin always allowed)."""

    async def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role == Role.ADMINISTRATOR:
            return current_user
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions for this action",
            )
        return current_user

    return role_checker


require_admin = require_roles(Role.ADMINISTRATOR)
require_field = require_roles(Role.FIELD_EXECUTIVE)
require_marketing = require_roles(Role.MARKETING_EXECUTIVE)
require_sales = require_roles(Role.SALES_EXECUTIVE)
require_manager = require_roles(Role.MANAGER)
require_ceo = require_roles(Role.CEO)
require_manager_or_ceo = require_roles(Role.MANAGER, Role.CEO)
