"""
Durable outbound event delivery ledger -- see docs/ROADMAP.md module 13's
event_outbox/delivery_status pieces. integrations/lead_sync_emitter.py is
fire-and-forget: a failed webhook POST is logged and the event is lost,
with no retry. This model gives every delivery attempt a persisted row so
services/outbox_service.py can retry with backoff and dead-letter after a
threshold, instead of silently dropping the sync.

The row's own id IS the envelope's eventId (extracted from the built
payload at enqueue time, not a fresh uuid4 minted by this model) -- every
retry of the same logical event reuses that identical id/eventId, which
is what makes idempotent replay on a future core-newax inbox meaningful.
"""

import enum
import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lead_harvester.database import Base


class OutboxStatus(str, enum.Enum):
    PENDING = "pending"
    DELIVERED = "delivered"
    FAILED = "failed"
    DEAD_LETTER = "dead_letter"


class EventOutbox(Base):
    """
    One row per outbound lead-sync event. PENDING rows with
    next_attempt_at in the past are eligible for
    outbox_service.process_pending_deliveries's claim query. A row moves
    PENDING -> DELIVERED on a successful POST, PENDING -> PENDING (with
    attempt_count incremented and next_attempt_at pushed out by the
    backoff schedule) on a retryable failure, or PENDING -> DEAD_LETTER
    once attempt_count reaches MAX_ATTEMPTS -- DEAD_LETTER is terminal and
    requires a human to requeue it (see api/routes/outbox.py), matching
    this codebase's terminal-state-completeness convention (see
    docs/CODE_REVIEW_LESSONS.md pattern 11).
    """

    __tablename__ = "event_outbox"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Nullable: every ordinary event is about a live institution, but
    # services/compliance_service.py::_erase_institution's own
    # "institution.deleted" tombstone event deliberately leaves this NULL
    # -- that institution is being deleted in the same transaction this
    # row is written in, and this FK's CASCADE (see migration
    # a5c7e9f1b3d5) would otherwise delete the tombstone right along with
    # it, before it can ever be delivered. The institution's id still
    # travels inside `payload` itself, which is all delivery needs.
    institution_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("canonical_institutions.id", ondelete="CASCADE"), nullable=True, index=True
    )

    # E.g. "institution.upserted" -- mirrors lead_sync_emitter.py's payload
    # eventType so a future inbox can dispatch on the same value.
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)

    # The exact signed envelope body (schemaVersion/eventId/eventType/
    # occurredAt/institution/branches/contactPoints) built once at enqueue
    # time -- every delivery attempt POSTs this identical payload, never a
    # freshly rebuilt one, so a retry can't drift from what was originally
    # queued.
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    status: Mapped[OutboxStatus] = mapped_column(
        Enum(OutboxStatus), default=OutboxStatus.PENDING, nullable=False, index=True
    )

    attempt_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # When this row next becomes eligible for a delivery attempt -- set to
    # "now" at enqueue (so the first attempt happens immediately) and
    # pushed forward by the backoff schedule after each failure.
    next_attempt_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False, index=True
    )

    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    institution = relationship("CanonicalInstitution")
