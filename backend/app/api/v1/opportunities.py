from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import uuid
from app.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.schemas.opportunity import (
    OpportunityCreate, OpportunityUpdate, OpportunityResponse,
    OpportunityTransition, LifecycleHistoryResponse, TransitionResponse,
    LeadTransferRequest, OpportunityDetailResponse, OpportunityOwnershipBrief,
)
from app.services.opportunity import OpportunityService

router = APIRouter()
service = OpportunityService()


class OwnershipResponse(BaseModel):
    id: uuid.UUID
    opportunity_id: uuid.UUID
    lead_creator_id: Optional[uuid.UUID] = None
    marketing_owner_id: Optional[uuid.UUID] = None
    sales_owner_id: Optional[uuid.UUID] = None
    revenue_credit: Optional[float] = None

    class Config:
        from_attributes = True


class OwnershipUpdate(BaseModel):
    marketing_owner_id: Optional[uuid.UUID] = None
    sales_owner_id: Optional[uuid.UUID] = None
    revenue_credit: Optional[float] = None


@router.post("/", response_model=OpportunityResponse)
def create_opportunity(
    data: OpportunityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    opp = service.create_opportunity(db, current_user, data)
    return OpportunityResponse.model_validate(opp)


@router.get("/", response_model=List[OpportunityResponse])
def list_opportunities(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    opps = service.list_opportunities(db, skip, limit)
    return [OpportunityResponse.model_validate(o) for o in opps]


@router.get("/{opportunity_id}/detail", response_model=OpportunityDetailResponse)
def get_opportunity_detail(
    opportunity_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    opp, history, ownership = service.get_opportunity_detail(db, opportunity_id)
    return OpportunityDetailResponse(
        opportunity=OpportunityResponse.model_validate(opp),
        history=[LifecycleHistoryResponse.model_validate(h) for h in history],
        ownership=OpportunityOwnershipBrief.model_validate(ownership) if ownership else None,
    )


@router.get("/{opportunity_id}", response_model=OpportunityResponse)
def get_opportunity(
    opportunity_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    opp = service.get_opportunity(db, opportunity_id)
    return OpportunityResponse.model_validate(opp)


@router.patch("/{opportunity_id}", response_model=OpportunityResponse)
def update_opportunity(
    opportunity_id: str,
    data: OpportunityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    opp = service.update_opportunity(db, current_user, opportunity_id, data)
    return OpportunityResponse.model_validate(opp)


@router.post("/{opportunity_id}/transition", response_model=TransitionResponse)
def transition_opportunity(
    opportunity_id: str,
    data: OpportunityTransition,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    result = service.transition(db, current_user, opportunity_id, data)
    return TransitionResponse(**result)


@router.get("/{opportunity_id}/history", response_model=List[LifecycleHistoryResponse])
def lifecycle_history(
    opportunity_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    history = service.get_lifecycle_history(db, opportunity_id)
    return [LifecycleHistoryResponse.model_validate(h) for h in history]


@router.get("/{opportunity_id}/ownership", response_model=OwnershipResponse)
def get_ownership(
    opportunity_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    record = service.get_ownership(db, opportunity_id)
    return OwnershipResponse.model_validate(record)


@router.post("/{opportunity_id}/lead-transfer", response_model=OpportunityResponse)
def lead_transfer(
    opportunity_id: str,
    data: LeadTransferRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    opp = service.lead_transfer(db, current_user, opportunity_id, data)
    return OpportunityResponse.model_validate(opp)


@router.patch("/{opportunity_id}/ownership", response_model=OwnershipResponse)
def update_ownership(
    opportunity_id: str,
    data: OwnershipUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    record = service.update_ownership(db, current_user, opportunity_id, data.model_dump(exclude_unset=True))
    return OwnershipResponse.model_validate(record)
