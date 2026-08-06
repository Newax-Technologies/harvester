"""
Tenant identity -- docs/ROADMAP.md Module 03 (Tenant and Workspace
Isolation) / docs/delivery/agency-intelligence-implementation-sequence.md
Slice 1.1.

This is a single-tier tenant boundary only. The full re-baselined model
(docs/architecture/agency-intelligence-rebaseline.md) also wants a
client-workspace tier nested under an agency/provider tenant -- that is
deliberately not built yet. A Workspace table can be added and given its
own foreign key on the tables this migration touches without changing
Tenant's shape or breaking the boundary that already exists once this
lands; skipping straight to a two-tier model in the same change would
double the blast radius of an already-wide migration for no immediate
enforcement benefit.

DEFAULT_TENANT_ID is the fixed identity every currently-single-tenant
installation is migrated into (see migrations/versions for the
tenant_id backfill), and the identity every model default and CLI
convenience flag falls back to until real multi-tenant onboarding
(Module 59) exists. It is not a placeholder to design around long-term.
"""

from __future__ import annotations

import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from lead_harvester.database import Base

DEFAULT_TENANT_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")
DEFAULT_TENANT_NAME = "Default Tenant"
DEFAULT_TENANT_SLUG = "default"


class TenantStatus(str, enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    status: Mapped[TenantStatus] = mapped_column(
        Enum(TenantStatus), default=TenantStatus.ACTIVE, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
