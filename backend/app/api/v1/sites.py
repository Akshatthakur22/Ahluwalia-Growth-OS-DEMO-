from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.schemas.site import (
    SiteCaptureCreate, SiteCaptureUpdate, SiteResponse, SiteDetailResponse,
    SiteMediaCreate, SiteMediaResponse,
    SiteLookupItem, SiteWithPipelineResponse, SitePipelineItem,
)
from app.schemas.contact import ContactResponse
from app.services.site import SiteService

router = APIRouter()
service = SiteService()


def _site_detail_response(db: Session, site_id: str) -> SiteDetailResponse:
    site, contacts, stakeholders, media = service.get_site_detail(db, site_id)
    return SiteDetailResponse(
        **SiteResponse.model_validate(site).model_dump(),
        contacts=[ContactResponse.model_validate(c) for c in contacts],
        stakeholders=stakeholders,
        media=[SiteMediaResponse.model_validate(m) for m in media],
    )


@router.post("/capture", response_model=SiteDetailResponse)
def capture_site(
    data: SiteCaptureCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    site = service.create_site(db, current_user, data)
    return _site_detail_response(db, str(site.id))


@router.post("/", response_model=SiteResponse)
def create_site(
    data: SiteCaptureCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    site = service.create_site(db, current_user, data)
    return SiteResponse.model_validate(site)


@router.get("/lookup", response_model=List[SiteLookupItem])
def list_sites_lookup(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    sites = service.list_lookup(db, current_user)
    return [SiteLookupItem.model_validate(s) for s in sites]


@router.get("/with-pipeline", response_model=SiteWithPipelineResponse)
def list_sites_with_pipeline(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    sites, opp_map = service.list_with_pipeline(db, current_user)
    return SiteWithPipelineResponse(
        sites=[SiteResponse.model_validate(s) for s in sites],
        opportunities_by_site={
            sid: SitePipelineItem(
                id=opp.id,
                opportunity_name=opp.opportunity_name,
                current_status=opp.current_status,
                expected_revenue=opp.expected_revenue,
            )
            for sid, opp in opp_map.items()
        },
    )


@router.get("/", response_model=List[SiteResponse])
def list_sites(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    sites = service.list_sites(db, current_user, skip, limit)
    return [SiteResponse.model_validate(s) for s in sites]


@router.get("/{site_id}/detail", response_model=SiteDetailResponse)
def get_site_detail(
    site_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return _site_detail_response(db, site_id)


@router.get("/{site_id}", response_model=SiteResponse)
def get_site(
    site_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    site = service.get_site(db, site_id)
    return SiteResponse.model_validate(site)


@router.patch("/{site_id}/capture", response_model=SiteDetailResponse)
def update_site_capture(
    site_id: str,
    data: SiteCaptureUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    service.update_site(db, current_user, site_id, data)
    return _site_detail_response(db, site_id)


@router.patch("/{site_id}", response_model=SiteResponse)
def update_site(
    site_id: str,
    data: SiteCaptureUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    site = service.update_site(db, current_user, site_id, data)
    return SiteResponse.model_validate(site)


@router.post("/{site_id}/media/upload", response_model=SiteMediaResponse)
async def upload_media_file(
    site_id: str,
    file: UploadFile = File(...),
    latitude: Optional[str] = Form(None),
    longitude: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    media = await service.upload_media_file(db, current_user, site_id, file, latitude, longitude)
    return SiteMediaResponse.model_validate(media)


@router.post("/{site_id}/media", response_model=SiteMediaResponse)
def upload_media(
    site_id: str,
    data: SiteMediaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    media = service.add_media(db, current_user, site_id, data)
    return SiteMediaResponse.model_validate(media)


@router.get("/{site_id}/media", response_model=List[SiteMediaResponse])
def list_media(
    site_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    media = service.get_media(db, site_id)
    return [SiteMediaResponse.model_validate(m) for m in media]
