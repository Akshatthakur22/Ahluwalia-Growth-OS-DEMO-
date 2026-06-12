import json
from typing import Any, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.audit import AuditLog


class AuditService:
    """Records immutable audit trail entries for critical actions."""

    def log(
        self,
        db: Session,
        *,
        user_id: Optional[UUID],
        entity_type: str,
        entity_id: UUID,
        action: str,
        previous_value: Any = None,
        new_value: Any = None,
        ip_address: Optional[str] = None,
        device_information: Optional[str] = None,
    ) -> AuditLog:
        entry = AuditLog(
            user_id=user_id,
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            previous_value=json.dumps(previous_value, default=str) if previous_value is not None else None,
            new_value=json.dumps(new_value, default=str) if new_value is not None else None,
            ip_address=ip_address,
            device_information=device_information,
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
