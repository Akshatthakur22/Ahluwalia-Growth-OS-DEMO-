from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.permissions import require_admin
from app.models.user import User
from app.schemas.audit import AuditLogResponse
from app.repositories.audit import AuditRepository

router = APIRouter()
repo = AuditRepository()


@router.get("/", response_model=List[AuditLogResponse])
def list_audit_logs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    logs = repo.get_multi(db, skip, limit)
    return [AuditLogResponse.model_validate(log) for log in logs]
