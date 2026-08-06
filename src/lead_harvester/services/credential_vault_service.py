"""
Write-only-by-default storage for connector/source credentials --
docs/ROADMAP.md Module 09 / docs/delivery/
agency-intelligence-implementation-sequence.md Slice 2.1.

store_credential() doubles as both "issue" and "rotate": called for a
(tenant_id, name) that has never been stored, it creates version 1;
called again for the same pair, it deactivates the current version and
inserts a new one -- identical versioning shape to
tenant_config_service.set_tenant_config, including the same
transaction-scoped advisory lock so two concurrent stores for a brand
new (tenant_id, name) pair can't race the partial unique index.

Only retrieve_plaintext_for_use() ever decrypts. Every other read
(get_credential_fingerprint, list_credentials) exposes metadata/
fingerprint only -- "no plaintext retrieval" (Slice 2.1's stated
deliverable) means there is deliberately no general-purpose getter that
hands back the secret value; a caller that genuinely needs to use the
credential (an actual connector making an API call, once Slice 2.2/2.3
exist) must call the one function whose name says what it does.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.tenancy import Tenant
from lead_harvester.models.vault import VaultedCredential
from lead_harvester.services.auth_service import TenantNotFoundError
from lead_harvester.vault_crypto import decrypt_secret, encrypt_secret, fingerprint_secret


async def _lock_and_get_active(
    session: AsyncSession, tenant_id: uuid.UUID, name: str
) -> VaultedCredential | None:
    # Same reasoning as tenant_config_service.set_tenant_config's lock:
    # needed even for the never-stored-before case, where there is no row
    # yet for a SELECT ... FOR UPDATE to lock.
    await session.execute(
        select(func.pg_advisory_xact_lock(func.hashtext(str(tenant_id)), func.hashtext(name)))
    )
    return (
        await session.scalars(
            select(VaultedCredential).where(
                VaultedCredential.tenant_id == tenant_id,
                VaultedCredential.name == name,
                VaultedCredential.is_active.is_(True),
            )
        )
    ).first()


async def store_credential(
    session: AsyncSession,
    tenant_id: uuid.UUID,
    name: str,
    plaintext_value: str,
    *,
    created_by: str,
) -> VaultedCredential:
    """
    Encrypts and stores `plaintext_value` as the new active version for
    (tenant_id, name). Raises TenantNotFoundError if tenant_id matches no
    Tenant row.
    """
    if await session.get(Tenant, tenant_id) is None:
        raise TenantNotFoundError(f"No tenant found with id {tenant_id}.")

    previous_active = await _lock_and_get_active(session, tenant_id, name)

    next_version = 1
    if previous_active is not None:
        previous_active.is_active = False
        next_version = previous_active.version + 1
    else:
        highest = await session.scalar(
            select(VaultedCredential.version)
            .where(VaultedCredential.tenant_id == tenant_id, VaultedCredential.name == name)
            .order_by(VaultedCredential.version.desc())
            .limit(1)
        )
        if highest is not None:
            next_version = highest + 1

    credential = VaultedCredential(
        tenant_id=tenant_id,
        name=name,
        fingerprint=fingerprint_secret(plaintext_value),
        ciphertext=encrypt_secret(plaintext_value),
        version=next_version,
        is_active=True,
        created_by=created_by,
    )
    session.add(credential)
    await session.flush()
    return credential


async def revoke_credential(
    session: AsyncSession, tenant_id: uuid.UUID, name: str
) -> VaultedCredential | None:
    """
    Deactivates the active version for (tenant_id, name) with no
    replacement -- the credential identity is dead until store_credential
    is called again under the same name, which starts a fresh version
    sequence. Returns the revoked row, or None if there was no active
    credential to revoke.
    """
    active = (
        await session.scalars(
            select(VaultedCredential).where(
                VaultedCredential.tenant_id == tenant_id,
                VaultedCredential.name == name,
                VaultedCredential.is_active.is_(True),
            )
        )
    ).first()
    if active is None:
        return None
    active.is_active = False
    active.revoked_at = datetime.now(UTC)
    return active


async def get_credential_fingerprint(
    session: AsyncSession, tenant_id: uuid.UUID, name: str
) -> str | None:
    """Fingerprint of the active credential for (tenant_id, name), or None if there isn't one."""
    return await session.scalar(
        select(VaultedCredential.fingerprint).where(
            VaultedCredential.tenant_id == tenant_id,
            VaultedCredential.name == name,
            VaultedCredential.is_active.is_(True),
        )
    )


@dataclass(frozen=True)
class CredentialSummary:
    """Metadata-only view of a VaultedCredential -- deliberately has no ciphertext field to leak."""

    name: str
    fingerprint: str
    version: int
    created_at: datetime
    created_by: str


async def list_credentials(session: AsyncSession, tenant_id: uuid.UUID) -> list[CredentialSummary]:
    """
    Every active credential for a tenant -- metadata/fingerprint only.
    Selects only the safe columns (not `select(VaultedCredential)`) so a
    caller can never reach `.ciphertext` through the returned rows, by
    construction rather than by convention.
    """
    rows = await session.execute(
        select(
            VaultedCredential.name,
            VaultedCredential.fingerprint,
            VaultedCredential.version,
            VaultedCredential.created_at,
            VaultedCredential.created_by,
        )
        .where(VaultedCredential.tenant_id == tenant_id, VaultedCredential.is_active.is_(True))
        .order_by(VaultedCredential.name.asc())
    )
    return [CredentialSummary(*row) for row in rows.all()]


async def retrieve_plaintext_for_use(session: AsyncSession, tenant_id: uuid.UUID, name: str) -> str:
    """
    The one sanctioned way to recover a vaulted credential's plaintext --
    for an actual connector/source that needs the real value to make a
    call, not for display, logging, or export. Raises ValueError if no
    active credential exists for (tenant_id, name).
    """
    active = (
        await session.scalars(
            select(VaultedCredential).where(
                VaultedCredential.tenant_id == tenant_id,
                VaultedCredential.name == name,
                VaultedCredential.is_active.is_(True),
            )
        )
    ).first()
    if active is None:
        raise ValueError(f"No active vaulted credential named {name!r} for tenant {tenant_id}.")
    return decrypt_secret(active.ciphertext)


def credential_metadata(credential: VaultedCredential) -> dict[str, Any]:
    """Safe-to-print summary of a VaultedCredential -- never includes ciphertext or plaintext."""
    return {
        "name": credential.name,
        "fingerprint": credential.fingerprint,
        "version": credential.version,
        "created_at": credential.created_at.isoformat(),
        "created_by": credential.created_by,
    }
