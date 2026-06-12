from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.schemas.contact import ContactResponse
from app.schemas.site import SiteResponse
from app.schemas.meeting import MeetingResponse
from app.schemas.showroom_visit import ShowroomVisitResponse
from app.schemas.opportunity import OpportunityResponse


class OwnerInfo(BaseModel):
    id: str
    name: Optional[str] = None
    role: Optional[str] = None


class OpportunityOwnership(BaseModel):
    opportunity: OpportunityResponse
    ownership: Dict[str, OwnerInfo] = {}


class MobileSearchResponse(BaseModel):
    mobile_number: str
    contacts: List[ContactResponse]
    sites: List[SiteResponse]
    meetings: List[MeetingResponse]
    showroom_visits: List[ShowroomVisitResponse]
    opportunities: List[OpportunityResponse]
    opportunity_ownership: List[OpportunityOwnership] = []


class NameSearchResponse(BaseModel):
    query: str
    contacts: List[ContactResponse]
    opportunities: List[OpportunityResponse] = []
    opportunity_ownership: List[OpportunityOwnership] = []


class SearchSuggestion(BaseModel):
    type: str
    label: str
    sublabel: str
    mobile: Optional[str] = None
    contact_id: Optional[str] = None


class SuggestResponse(BaseModel):
    suggestions: List[SearchSuggestion]
