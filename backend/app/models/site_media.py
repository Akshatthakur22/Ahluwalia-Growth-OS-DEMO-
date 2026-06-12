from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel


class SiteMedia(BaseModel):
    """
    Site media model for storing supporting evidence.
    """
    __tablename__ = "site_media"
    
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False, index=True)
    media_type = Column(String(50), nullable=False)
    file_url = Column(String(1000), nullable=False)
    latitude = Column(String(50), nullable=True)
    longitude = Column(String(50), nullable=True)
    captured_at = Column(DateTime(timezone=True), nullable=True)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
