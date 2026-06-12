from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.schemas.assignment import AssignmentCreate, AssignmentResponse
from app.services.assignment import AssignmentService

router = APIRouter()
service = AssignmentService()


@router.post("/", response_model=AssignmentResponse)
def create_assignment(
    data: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    assignment = service.create_assignment(db, current_user, data)
    return AssignmentResponse.model_validate(assignment)


@router.get("/", response_model=List[AssignmentResponse])
def list_assignments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    assignments = service.list_assignments(db, current_user, skip, limit)
    return [AssignmentResponse.model_validate(a) for a in assignments]
