from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.schemas.attendance import (
    CheckInRequest, CheckOutRequest, CheckInResponse, AttendanceResponse,
    TeamAttendanceResponse, TodayStatusResponse, AttendanceSummaryResponse,
    TeamAttendanceSummaryResponse, AttendancePageDataResponse,
    TeamAttendancePageDataResponse,
)
from app.services.attendance import AttendanceService

router = APIRouter()
service = AttendanceService()


@router.post("/check-in", response_model=CheckInResponse)
def check_in(
    data: CheckInRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    record = service.check_in(db, current_user, data)
    return CheckInResponse(attendance_status="checked_in", check_in_time=record.check_in_time, id=record.id)


@router.post("/check-out", response_model=AttendanceResponse)
def check_out(
    data: CheckOutRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    record = service.check_out(db, current_user, data)
    return AttendanceResponse.model_validate(record)


@router.get("/page-data", response_model=AttendancePageDataResponse)
def my_page_data(
    skip: int = 0,
    limit: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    data = service.get_my_page_data(db, current_user, skip, limit)
    record = data["today"]["record"]
    return AttendancePageDataResponse(
        today=TodayStatusResponse(
            checked_in=data["today"]["checked_in"],
            checked_out=data["today"]["checked_out"],
            record=AttendanceResponse.model_validate(record) if record else None,
        ),
        summary=AttendanceSummaryResponse(**data["summary"]),
        records=[AttendanceResponse.model_validate(r) for r in data["records"]],
    )


@router.get("/today", response_model=TodayStatusResponse)
def today_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    data = service.get_today_status(db, current_user)
    record = data["record"]
    return TodayStatusResponse(
        checked_in=data["checked_in"],
        checked_out=data["checked_out"],
        record=AttendanceResponse.model_validate(record) if record else None,
    )


@router.get("/my-summary", response_model=AttendanceSummaryResponse)
def my_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return AttendanceSummaryResponse(**service.get_my_summary(db, current_user))


@router.get("/my-attendance", response_model=List[AttendanceResponse])
def my_attendance(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    records = service.get_my_attendance(db, current_user, skip, limit)
    return [AttendanceResponse.model_validate(r) for r in records]


@router.get("/team-page-data", response_model=TeamAttendancePageDataResponse)
def team_page_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    data = service.get_team_page_data(db, current_user)
    return TeamAttendancePageDataResponse(
        summary=TeamAttendanceSummaryResponse(**data["summary"]),
        today_records=[
            TeamAttendanceResponse(
                **AttendanceResponse.model_validate(log).model_dump(),
                employee_name=name,
                employee_code=code,
                role=role.value if role else None,
            )
            for log, name, code, role in data["today_records"]
        ],
    )


@router.get("/team", response_model=List[TeamAttendanceResponse])
def team_attendance(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    rows = service.get_team_attendance(db, current_user, skip, limit)
    return [
        TeamAttendanceResponse(
            **AttendanceResponse.model_validate(log).model_dump(),
            employee_name=name,
            employee_code=code,
            role=role.value if role else None,
        )
        for log, name, code, role in rows
    ]


@router.get("/team-summary", response_model=TeamAttendanceSummaryResponse)
def team_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return TeamAttendanceSummaryResponse(**service.get_team_summary(db, current_user))
