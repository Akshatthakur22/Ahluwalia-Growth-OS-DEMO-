from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.schemas.search import (
    MobileSearchResponse, NameSearchResponse, SuggestResponse,
    OpportunityOwnership, OwnerInfo,
)
from app.schemas.contact import ContactResponse
from app.schemas.site import SiteResponse
from app.schemas.meeting import MeetingResponse
from app.schemas.showroom_visit import ShowroomVisitResponse
from app.schemas.opportunity import OpportunityResponse
from app.services.search import SearchService

router = APIRouter()
service = SearchService()


def _map_ownership(items) -> list[OpportunityOwnership]:
    mapped = []
    for item in items:
        owners = {
            k: OwnerInfo(**v) for k, v in item["ownership"].items()
        }
        mapped.append(OpportunityOwnership(
            opportunity=OpportunityResponse.model_validate(item["opportunity"]),
            ownership=owners,
        ))
    return mapped


@router.get("/suggest", response_model=SuggestResponse)
def search_suggest(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    suggestions = service.suggest(db, q)
    return SuggestResponse(suggestions=suggestions)


@router.get("/mobile/{mobile_number}", response_model=MobileSearchResponse)
def search_by_mobile(
    mobile_number: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    result = service.search_by_mobile(db, mobile_number)
    return MobileSearchResponse(
        mobile_number=result["mobile_number"],
        contacts=[ContactResponse.model_validate(c) for c in result["contacts"]],
        sites=[SiteResponse.model_validate(s) for s in result["sites"]],
        meetings=[MeetingResponse.model_validate(m) for m in result["meetings"]],
        showroom_visits=[ShowroomVisitResponse.model_validate(v) for v in result["showroom_visits"]],
        opportunities=[OpportunityResponse.model_validate(o) for o in result["opportunities"]],
        opportunity_ownership=_map_ownership(result.get("opportunity_ownership", [])),
    )


@router.get("/name/{name}", response_model=NameSearchResponse)
def search_by_name(
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    result = service.search_by_name(db, name)
    return NameSearchResponse(
        query=result["query"],
        contacts=[ContactResponse.model_validate(c) for c in result["contacts"]],
        opportunities=[OpportunityResponse.model_validate(o) for o in result.get("opportunities", [])],
        opportunity_ownership=_map_ownership(result.get("opportunity_ownership", [])),
    )
