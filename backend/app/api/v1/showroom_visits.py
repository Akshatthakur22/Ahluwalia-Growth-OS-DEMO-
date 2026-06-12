from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.schemas.showroom_visit import ShowroomVisitCreate, ShowroomVisitUpdate, ShowroomVisitResponse
from app.services.showroom_visit import ShowroomVisitService

router = APIRouter()
service = ShowroomVisitService()


@router.post("/", response_model=ShowroomVisitResponse)
def create_visit(
    data: ShowroomVisitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    visit = service.create_visit(db, current_user, data)
    return ShowroomVisitResponse.model_validate(visit)


@router.get("/", response_model=List[ShowroomVisitResponse])
def list_visits(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    visits = service.list_visits(db, current_user, skip, limit)
    return [ShowroomVisitResponse.model_validate(v) for v in visits]


@router.patch("/{visit_id}", response_model=ShowroomVisitResponse)
def update_visit(
    visit_id: str,
    data: ShowroomVisitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    visit = service.update_visit(db, current_user, visit_id, data)
    return ShowroomVisitResponse.model_validate(visit)
