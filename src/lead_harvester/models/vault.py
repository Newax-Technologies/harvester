"""
Vaulted (encrypted) credential storage -- docs/ROADMAP.md Module 09 /
docs/delivery/agency-intelligence-implementation-sequence.md Slice 2.1.

Same versioned-row shape as models/tenant_config.py's TenantConfigOverride
(a row is never updated in place -- rotating or revoking inserts/flags a
new state and history is preserved), but for connector/source secrets
instead of plain config values, and the `value` column is Fernet
ciphertext (vault_crypto.py) rather than a JSONB scalar.

`is_active` distinguishes the two ways a version stops being current:
rotating sets is_active=False on the row it replaces and leaves
revoked_at null (superseded, not revoked -- the credential identity
itself is still alive, just on a newer value). Revoking sets both
is_active=False and revoked_at on the current row with no replacement
row inserted (the credential identity itself is dead until someone
issues a new one under the same tenant/name, which starts a fresh
version sequence the same way ServiceCredential's name reuse does).
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from lead_harvester.database import Base


class VaultedCredential(Base):
    __tablename__ = "vaulted_credentials"

    __table_args__ = (
        # Exactly one ACTIVE version per (tenant_id, name) -- see
        # models/tenant_config.py's identical reasoning for why this must
        # be a partial index (postgresql_where), not a plain
        # UniqueConstraint across is_active too.
        Index(
            "uq_vaulted_credentials_one_active_version",
            "tenant_id",
            "name",
            unique=True,
            postgresql_where=text("is_active = true"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenants.id"), nullable=False, index=True
    )
    # What this secret is for, e.g. "google_places_api_key" or
    # "linkedin_burner_07_session" -- not a foreign key to any connector
    # table yet (Slice 2.2/2.3 haven't been built), just a stable string
    # identity within the tenant.
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    # SHA-256 hex digest of the plaintext -- see vault_crypto.fingerprint_secret.
    # Lets an operator verify identity without decrypting.
    fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    # Fernet ciphertext (vault_crypto.encrypt_secret) -- never plaintext.
    ciphertext: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    # ServiceCredential.name of whoever/whatever stored this version --
    # same convention as TenantConfigOverride.created_by.
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
