import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lead_harvester.database import Base


class VerificationStatus(str, enum.Enum):
    PENDING = "pending"
    VALID = "valid"
    INVALID = "invalid"
    RISKY = "risky"      # e.g. catch-all domain, disposable, role-based address
    UNKNOWN = "unknown"  # no verification provider configured, or the provider couldn't decide


class ContactVerification(Base):
    """
    Append-only audit trail of every verification attempt against a ContactPoint
    (mirrors the FieldProvenance / AuditLog pattern elsewhere in the schema).
    ContactPoint.verification_status/verified_at hold the latest result for
    fast filtering; this table keeps the full history of who/what asserted it.
    """
    __tablename__ = "contact_verifications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contact_point_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("contact_points.id"), nullable=False, index=True)

    # e.g. "local_heuristic", or the configured licensed provider's name
    provider: Mapped[str] = mapped_column(String(100), nullable=False)

    status: Mapped[VerificationStatus] = mapped_column(Enum(VerificationStatus), default=VerificationStatus.PENDING, nullable=False)

    is_disposable: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_role_account: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)  # e.g. info@, admin@
    mx_found: Mapped[bool | None] = mapped_column(nullable=True)

    raw_response = mapped_column(JSONB, default=dict, nullable=False)

    verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    contact_point = relationship("ContactPoint", back_populates="verifications")
