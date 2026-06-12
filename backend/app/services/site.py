import uuid
from typing import Optional
from datetime import datetime, timezone
from pathlib import Path
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from app.models.user import User, Role
from app.repositories.site import SiteRepository, SiteMediaRepository
from app.repositories.contact import ContactRepository
from app.repositories.opportunity import OpportunityRepository, OwnershipRepository
from app.models.opportunity import OpportunityStatus
from app.schemas.site import SiteCaptureCreate, SiteCaptureUpdate, SiteMediaCreate, StakeholderFields
from app.services.audit import AuditService

UPLOAD_ROOT = Path(__file__).resolve().parents[2] / "uploads" / "sites"
STAKEHOLDER_KEYS = ("owner", "builder", "architect")


class SiteService:
    def __init__(self):
        self.repo = SiteRepository()
        self.media_repo = SiteMediaRepository()
        self.contact_repo = ContactRepository()
        self.opportunity_repo = OpportunityRepository()
        self.ownership_repo = OwnershipRepository()
        self.audit = AuditService()

    def _site_payload(self, data) -> dict:
        exclude = {
            "owner_name", "owner_mobile", "owner_address",
            "builder_name", "builder_firm_name", "builder_mobile", "builder_category",
            "architect_name", "architect_firm_name", "architect_mobile", "architect_category",
        }
        if hasattr(data, "model_dump"):
            raw = data.model_dump(exclude_unset=True)
        else:
            raw = dict(data)
        return {k: v for k, v in raw.items() if k not in exclude}

    def _stakeholder_payload(self, data) -> dict:
        if hasattr(data, "model_dump"):
            d = data.model_dump()
        else:
            d = dict(data)
        return {
            "owner": {
                "name": d.get("owner_name"),
                "mobile_number": d.get("owner_mobile"),
                "address": d.get("owner_address"),
            },
            "builder": {
                "name": d.get("builder_name"),
                "mobile_number": d.get("builder_mobile"),
                "firm_name": d.get("builder_firm_name"),
                "category": d.get("builder_category"),
            },
            "architect": {
                "name": d.get("architect_name"),
                "mobile_number": d.get("architect_mobile"),
                "firm_name": d.get("architect_firm_name"),
                "category": d.get("architect_category"),
            },
        }

    def _sync_stakeholders(self, db: Session, site_id, stakeholders: dict):
        for contact_type in STAKEHOLDER_KEYS:
            fields = stakeholders.get(contact_type, {})
            name = fields.get("name")
            mobile = fields.get("mobile_number")
            if not name or not mobile:
                continue
            payload = {
                "name": name,
                "mobile_number": mobile,
                "contact_type": contact_type,
                "address": fields.get("address"),
                "firm_name": fields.get("firm_name"),
                "category": fields.get("category"),
            }
            payload = {k: v for k, v in payload.items() if v is not None}
            existing = self.contact_repo.get_by_site_and_type(db, site_id, contact_type)
            if existing:
                self.contact_repo.update(db, existing, payload)
            else:
                self.contact_repo.create(db, {"site_id": site_id, **payload})

    def contacts_to_stakeholder_fields(self, contacts) -> StakeholderFields:
        by_type = {c.contact_type: c for c in contacts}
        owner = by_type.get("owner")
        builder = by_type.get("builder")
        architect = by_type.get("architect")
        return StakeholderFields(
            owner_name=owner.name if owner else None,
            owner_mobile=owner.mobile_number if owner else None,
            owner_address=owner.address if owner else None,
            builder_name=builder.name if builder else None,
            builder_firm_name=builder.firm_name if builder else None,
            builder_mobile=builder.mobile_number if builder else None,
            builder_category=builder.category if builder else None,
            architect_name=architect.name if architect else None,
            architect_firm_name=architect.firm_name if architect else None,
            architect_mobile=architect.mobile_number if architect else None,
            architect_category=architect.category if architect else None,
        )

    def create_site(self, db: Session, user: User, data: SiteCaptureCreate):
        site_data = self._site_payload(data)
        site_data["discovered_by"] = user.id
        site = self.repo.create(db, site_data)
        self._sync_stakeholders(db, site.id, self._stakeholder_payload(data))

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

    def update_site(self, db: Session, user: User, site_id: str, data: SiteCaptureUpdate):
        site = self.get_site(db, site_id)
        update_data = self._site_payload(data)
        if update_data:
            site = self.repo.update(db, site, update_data)
        stakeholders = self._stakeholder_payload(data)
        if any(stakeholders[t].get("name") for t in STAKEHOLDER_KEYS):
            self._sync_stakeholders(db, site.id, stakeholders)
        self.audit.log(db, user_id=user.id, entity_type="site", entity_id=site.id, action="update", new_value=update_data)
        return site

    def get_site_detail(self, db: Session, site_id: str, include_media: bool = True):
        site = self.get_site(db, site_id)
        contacts = self.contact_repo.get_by_site(db, site_id)
        media = self.media_repo.get_by_site(db, site_id) if include_media else []
        return site, contacts, self.contacts_to_stakeholder_fields(contacts), media

    def list_sites(self, db: Session, user: User, skip: int = 0, limit: int = 100):
        limit = min(limit, 200)
        if user.role in (Role.MANAGER, Role.CEO, Role.ADMINISTRATOR):
            return self.repo.get_multi(db, skip, limit)
        if user.role == Role.FIELD_EXECUTIVE:
            return self.repo.get_by_discoverer(db, user.id, skip, limit)
        return self.repo.get_multi(db, skip, limit)

    def list_lookup(self, db: Session, user: User):
        return self.list_sites(db, user, 0, 500)

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

    def add_media(self, db: Session, user: User, site_id: str, data: SiteMediaCreate):
        self.get_site(db, site_id)
        media = self.media_repo.create(db, {
            "site_id": site_id,
            "media_type": data.media_type,
            "file_url": data.file_url,
            "latitude": data.latitude,
            "longitude": data.longitude,
            "captured_at": data.captured_at or datetime.now(timezone.utc),
            "uploaded_by": user.id,
        })
        self.audit.log(db, user_id=user.id, entity_type="site_media", entity_id=media.id, action="upload", new_value=data.model_dump(mode="json"))
        return media

    async def upload_media_file(
        self,
        db: Session,
        user: User,
        site_id: str,
        file: UploadFile,
        latitude: Optional[str] = None,
        longitude: Optional[str] = None,
    ):
        self.get_site(db, site_id)
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only image files are allowed")

        UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
        ext = Path(file.filename or "photo.jpg").suffix or ".jpg"
        filename = f"{uuid.uuid4()}{ext}"
        dest = UPLOAD_ROOT / filename

        content = await file.read()
        if len(content) > 8 * 1024 * 1024:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image must be under 8MB")
        dest.write_bytes(content)

        file_url = f"/uploads/sites/{filename}"
        return self.add_media(db, user, site_id, SiteMediaCreate(
            media_type="site_photo",
            file_url=file_url,
            latitude=latitude,
            longitude=longitude,
            captured_at=datetime.now(timezone.utc),
        ))

    def get_media(self, db: Session, site_id: str):
        self.get_site(db, site_id)
        return self.media_repo.get_by_site(db, site_id)
