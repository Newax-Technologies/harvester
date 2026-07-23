import enum
import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import String, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from lead_harvester.database import Base


class AuditLog(Base):
    """
    A unified audit trail for all human and system mutations.
    Required for a human-in-the-loop system to track 'who did what'.
    """
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # E.g. 'draft.edited', 'draft.approved', 'resolution.merged'
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    
    # E.g. 'admin-user', 'system', 'reviewer'
    actor: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # E.g. 'OutreachDraft', 'ResolutionCandidate'
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Delta of the change
    previous_state = mapped_column(JSONB, nullable=True)
    new_state = mapped_column(JSONB, nullable=True)
    
    # E.g. "Observation verified against official admissions page."
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    
    # Optional request correlation ID for tracing
    request_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
