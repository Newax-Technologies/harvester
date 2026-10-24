"""
Service credentials -- the identity boundary for api/dependencies.py's
get_current_user(). Replaces the two hardcoded bearer-token literals
("secret-admin-token"/"secret-reviewer-token") that used to live directly
in dependencies.py, and the silent "unrecognized token -> viewer" fallback
that meant any string at all authenticated as a real, if low-privileged,
user.

Only a SHA-256 digest of the raw token is ever stored (see
services/auth_service.py::hash_token) -- the raw token itself is shown to
the operator exactly once, at issuance (cli.py's issue-service-credential
command), matching the write-only credential pattern used elsewhere in
this codebase (docs/ROADMAP.md Module 09).

Implements the "removal of hard-coded production tokens" and "session
lifecycle, expiry, revocation, reauthentication" deliverables of
docs/delivery/agency-intelligence-implementation-sequence.md Slice 1.2.
Real SSO/OIDC integration remains a separate, later decision -- this table
is the boundary such a token exchange would populate, not a replacement
for it.
"""

from __future__ import annotations

import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from lead_harvester.database import Base
from lead_harvester.models.tenancy import DEFAULT_TENANT_ID


class ServiceRole(str, enum.Enum):
    ADMIN = "admin"
    REVIEWER = "reviewer"
    VIEWER = "viewer"


class ServiceCredential(Base):
    __tablename__ = "service_credentials"

    # Partial unique index instead of a table-wide unique constraint on
    # name -- revoked_at is set (never cleared) on revoke, never on
    # delete, so name must only stay unique among ACTIVE (non-revoked)
    # credentials. Otherwise re-issuing a replacement under the same
    # identity after revoking a lost token (see cli.py's own "re-run to
    # issue a replacement" guidance) would permanently fail on this
    # constraint. Matches the partial index created in migration
    # a5c7e9b1d3f5_add_service_credentials.py.
    __table_args__ = (
        Index(
            "uq_service_credentials_active_name",
            "name",
            unique=True,
            postgresql_where=text("revoked_at IS NULL"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Which tenant this identity acts as -- api/dependencies.py::User
    # carries it forward from here on every authenticated request so
    # tenant-scoped queries (services/institution_service.py, for now)
    # have a source of truth that isn't client-supplied.
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenants.id"), nullable=False, index=True, default=DEFAULT_TENANT_ID
    )
    # Human-readable identity of who/what holds this credential (e.g.
    # "alice@newax.co", "ci-export-worker") -- becomes User.username.
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[ServiceRole] = mapped_column(Enum(ServiceRole), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # Set (never cleared) to revoke -- authenticate_token() rejects any
    # credential with a non-null revoked_at regardless of expires_at.
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
