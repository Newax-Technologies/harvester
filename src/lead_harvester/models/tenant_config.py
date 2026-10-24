"""
Versioned per-tenant configuration overrides -- docs/ROADMAP.md Module 07
/ delivery sequence Slice 1.4. See config_registry.py for the whitelist
of keys a row here may hold and their declared types/defaults.

A row is never updated in place -- setting a key inserts a new row with
version = previous_max + 1 and is_active=True, and flips the prior active
row (if any) to is_active=False in the same transaction. This preserves
full configuration history (Slice 1.4's "safe defaults and configuration
history" deliverable) rather than only ever showing the current value.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from lead_harvester.database import Base


class TenantConfigOverride(Base):
    __tablename__ = "tenant_config_overrides"

    __table_args__ = (
        # Exactly one ACTIVE version per (tenant, key) -- a plain
        # UniqueConstraint on (tenant_id, key, is_active) would also cap
        # every tenant/key pair at a single is_active=False row, breaking
        # history. Partial index (same pattern as ServiceCredential.name's
        # uq_service_credentials_active_name) restricts uniqueness to
        # is_active=True rows only.
        Index(
            "uq_tenant_config_one_active_version",
            "tenant_id",
            "key",
            unique=True,
            postgresql_where=text("is_active = true"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenants.id"), nullable=False, index=True
    )
    key: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    value: Mapped[dict] = mapped_column(JSONB, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    # See __table_args__'s UniqueConstraint -- only ever True for the
    # single most recent version of a given (tenant_id, key). Older
    # versions are set to False, never deleted.
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    # ServiceCredential.name of whoever/whatever set this version --
    # plain string like AuditLog.actor, not a foreign key, so history
    # survives the credential itself being revoked or renamed later.
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
