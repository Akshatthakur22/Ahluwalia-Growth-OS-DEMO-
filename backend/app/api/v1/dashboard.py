from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_active_user
from app.core.permissions import require_ceo, require_manager
from app.models.user import User
from app.schemas.dashboard import ExecutiveDashboard, ManagerDashboard, RoleDashboard
from app.services.dashboard import DashboardService

router = APIRouter()
service = DashboardService()


@router.get("/executive", response_model=ExecutiveDashboard)
def executive_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_ceo),
):
    return ExecutiveDashboard(**service.get_executive_dashboard(db))


@router.get("/manager", response_model=ManagerDashboard)
def manager_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_manager),
):
    return ManagerDashboard(**service.get_manager_dashboard(db))


@router.get("/role", response_model=RoleDashboard)
def role_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return RoleDashboard(**service.get_role_dashboard(db, current_user))
