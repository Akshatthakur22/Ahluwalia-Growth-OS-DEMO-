from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.schemas.meeting import MeetingCreate, MeetingUpdate, MeetingResponse
from app.services.meeting import MeetingService

router = APIRouter()
service = MeetingService()


@router.post("/", response_model=MeetingResponse)
def create_meeting(
    data: MeetingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    meeting = service.create_meeting(db, current_user, data)
    return MeetingResponse.model_validate(meeting)


@router.get("/", response_model=List[MeetingResponse])
def list_meetings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    meetings = service.list_meetings(db, current_user, skip, limit)
    return [MeetingResponse.model_validate(m) for m in meetings]


@router.patch("/{meeting_id}", response_model=MeetingResponse)
def update_meeting(
    meeting_id: str,
    data: MeetingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    meeting = service.update_meeting(db, current_user, meeting_id, data)
    return MeetingResponse.model_validate(meeting)
