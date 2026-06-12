from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, Role
from app.repositories.site import SiteRepository, SiteMediaRepository
from app.repositories.opportunity import OpportunityRepository, OwnershipRepository
from app.models.opportunity import OpportunityStatus
from app.schemas.site import SiteCreate, SiteUpdate, SiteMediaCreate
from app.services.audit import AuditService


class SiteService:
    def __init__(self):
        self.repo = SiteRepository()
        self.media_repo = SiteMediaRepository()
        self.opportunity_repo = OpportunityRepository()
        self.ownership_repo = OwnershipRepository()
        self.audit = AuditService()

    def create_site(self, db: Session, user: User, data: SiteCreate):
        site_data = data.model_dump()
        site_data["discovered_by"] = user.id
        site = self.repo.create(db, site_data)

        opportunity = self.opportunity_repo.create(db, {
            "site_id": site.id,
            "opportunity_name": f"{site.site_name} - Opportunity",
            "current_status": OpportunityStatus.NEW_SITE.value,
        })
        self.ownership_repo.create(db, {
            "opportunity_id": opportunity.id,
            "lead_creator_id": user.id,
        })
        self.audit.log(db, user_id=user.id, entity_type="site", entity_id=site.id, action="create", new_value=site_data)
        return site

    def list_sites(self, db: Session, user: User, skip: int = 0, limit: int = 100):
        limit = min(limit, 200)
        if user.role in (Role.MANAGER, Role.CEO, Role.ADMINISTRATOR):
            return self.repo.get_multi(db, skip, limit)
        if user.role == Role.FIELD_EXECUTIVE:
            return self.repo.get_by_discoverer(db, user.id, skip, limit)
        return self.repo.get_multi(db, skip, limit)

    def list_lookup(self, db: Session, user: User):
        sites = self.list_sites(db, user, 0, 500)
        return sites

    def list_with_pipeline(self, db: Session, user: User):
        sites = self.list_sites(db, user, 0, 200)
        site_ids = [s.id for s in sites]
        opps = self.opportunity_repo.get_by_sites(db, site_ids)
        opp_by_site = {}
        for opp in opps:
            key = str(opp.site_id)
            if key not in opp_by_site:
                opp_by_site[key] = opp
        return sites, opp_by_site

    def get_site(self, db: Session, site_id: str):
        site = self.repo.get(db, site_id)
        if not site:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")
        return site

    def update_site(self, db: Session, user: User, site_id: str, data: SiteUpdate):
        site = self.get_site(db, site_id)
        update_data = data.model_dump(exclude_unset=True)
        updated = self.repo.update(db, site, update_data)
        self.audit.log(db, user_id=user.id, entity_type="site", entity_id=site.id, action="update", new_value=update_data)
        return updated

    def add_media(self, db: Session, user: User, site_id: str, data: SiteMediaCreate):
        self.get_site(db, site_id)
        media = self.media_repo.create(db, {
            "site_id": site_id,
            "media_type": data.media_type,
            "file_url": data.file_url,
            "uploaded_by": user.id,
        })
        self.audit.log(db, user_id=user.id, entity_type="site_media", entity_id=media.id, action="upload", new_value=data.model_dump())
        return media

    def get_media(self, db: Session, site_id: str):
        self.get_site(db, site_id)
        return self.media_repo.get_by_site(db, site_id)
