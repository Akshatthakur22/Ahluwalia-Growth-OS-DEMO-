from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.site import Site
from app.models.site_media import SiteMedia
from app.repositories.base import BaseRepository


class SiteRepository(BaseRepository[Site]):
    def __init__(self):
        super().__init__(Site)

    def get_by_discoverer(self, db: Session, user_id, skip: int = 0, limit: int = 100) -> List[Site]:
        return (
            db.query(Site)
            .filter(Site.discovered_by == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


class SiteMediaRepository(BaseRepository[SiteMedia]):
    def __init__(self):
        super().__init__(SiteMedia)

    def get_by_site(self, db: Session, site_id) -> List[SiteMedia]:
        return db.query(SiteMedia).filter(SiteMedia.site_id == site_id).all()
