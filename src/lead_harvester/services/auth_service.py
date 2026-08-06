"""
Issues, authenticates, and revokes ServiceCredential rows -- see
models/auth.py's module docstring for why this replaces the previous
hardcoded bearer tokens in api/dependencies.py.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import secrets
import uuid

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.database import get_session
from lead_harvester.models.auth import ServiceCredential, ServiceRole
from lead_harvester.models.tenancy import DEFAULT_TENANT_ID, Tenant, TenantStatus


def hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def generate_raw_token() -> str:
    return secrets.token_urlsafe(32)


class TenantNotFoundError(ValueError):
    """Raised by issue_service_credential() when tenant_id matches no Tenant row."""


class TenantScopeIncompleteError(ValueError):
    """
    Raised by issue_service_credential() for any tenant_id other than
    DEFAULT_TENANT_ID. docs/delivery/agency-intelligence-implementation-sequence.md
    Slice 1.1 tenant-scopes CanonicalInstitution/Branch/ContactPoint (and
    reads through InstitutionService) only -- drafts, resolution reviews,
    dashboard, exports, and every other route/service still query
    globally. A credential actually authenticated as a non-default tenant
    would see and mutate every other tenant's data through those paths,
    so issuance is refused outright until they're scoped too, rather than
    letting the tenant_id column create the appearance of isolation that
    doesn't hold end to end.
    """


async def issue_service_credential(
    session: AsyncSession,
    *,
    name: str,
    role: ServiceRole,
    tenant_id: uuid.UUID = DEFAULT_TENANT_ID,
    expires_at: dt.datetime | None = None,
) -> tuple[ServiceCredential, str]:
    """
    Returns (credential, raw_token). raw_token is never persisted or
    logged anywhere -- the caller (cli.py's issue-service-credential
    command) must show it to the operator now, since it cannot be
    recovered later.

    Raises TenantScopeIncompleteError for any tenant_id other than
    DEFAULT_TENANT_ID -- see that class's docstring. Raises
    TenantNotFoundError if tenant_id (even DEFAULT_TENANT_ID) matches no
    Tenant row -- a mistyped, stale, or not-yet-migrated tenant would
    otherwise reach the tenant_id foreign key at flush and surface as an
    unhandled IntegrityError instead of a clean, catchable error.
    """
    if tenant_id != DEFAULT_TENANT_ID:
        raise TenantScopeIncompleteError(
            f"Cannot issue a credential for tenant {tenant_id} -- only the default tenant "
            f"({DEFAULT_TENANT_ID}) is currently safe to authenticate as. Tenant scoping only "
            "covers CanonicalInstitution/Branch/ContactPoint and InstitutionService's reads so "
            "far; every other route and service still queries across all tenants."
        )

    if await session.get(Tenant, tenant_id) is None:
        raise TenantNotFoundError(f"No tenant found with id {tenant_id}.")

    raw_token = generate_raw_token()
    credential = ServiceCredential(
        name=name,
        role=role,
        tenant_id=tenant_id,
        token_hash=hash_token(raw_token),
        expires_at=expires_at,
    )
    session.add(credential)
    await session.flush()
    return credential, raw_token


async def revoke_service_credential(session: AsyncSession, name: str) -> ServiceCredential | None:
    """Returns the revoked credential, or None if no active credential has this name."""
    credential = (
        await session.scalars(select(ServiceCredential).where(ServiceCredential.name == name))
    ).first()
    if credential is None or credential.revoked_at is not None:
        return None
    credential.revoked_at = dt.datetime.now(dt.UTC)
    return credential


async def _record_last_used(credential_id: uuid.UUID, when: dt.datetime) -> None:
    """
    Records last_used_at on its own short, independently-committed
    transaction rather than mutating the caller's session -- two reasons:
    (1) the caller's session belongs to the request that authenticated
    this token; if authorization later denies, or the route raises, that
    whole transaction rolls back and would silently discard this
    timestamp along with it, even though the token genuinely
    authenticated. (2) mutating this row on the shared request session
    holds a write lock on it for however long that request takes to
    finish -- with one token used by concurrent callers, that serializes
    otherwise-independent requests behind each other. A standalone
    update-and-commit here is held only as long as this one statement.
    """
    async with get_session() as session:
        await session.execute(
            update(ServiceCredential)
            .where(ServiceCredential.id == credential_id)
            .values(last_used_at=when)
            # This update runs against a different session than the one
            # that loaded `credential` in authenticate_token() -- there is
            # no in-memory ORM object here for SQLAlchemy to reconcile
            # against, so ask for the plain, predictable bulk-UPDATE
            # behavior rather than the "evaluate"/"fetch" auto-sync
            # strategies meant for same-session in-memory consistency.
            .execution_options(synchronize_session=False)
        )


async def authenticate_token(session: AsyncSession, raw_token: str) -> ServiceCredential | None:
    """
    Returns the matching credential if it exists, is not revoked, has not
    expired, and belongs to an ACTIVE tenant -- None otherwise. A
    successful match records last_used_at on a separate row (see
    _record_last_used) -- the returned object's own last_used_at
    attribute reflects its state as loaded, i.e. from before this call,
    not the timestamp this call just recorded. Never raises for an
    unknown/invalid token; the caller (api/dependencies.py::get_current_user)
    turns a None result into a 401.
    """
    token_hash = hash_token(raw_token)
    credential = (
        await session.scalars(
            select(ServiceCredential).where(ServiceCredential.token_hash == token_hash)
        )
    ).first()
    if credential is None or credential.revoked_at is not None:
        return None

    now = dt.datetime.now(dt.UTC)
    if credential.expires_at is not None and credential.expires_at <= now:
        return None

    # A credential is only as trustworthy as its tenant -- suspending a
    # tenant must terminate every one of its credentials' access
    # immediately, without requiring each one to be individually revoked.
    tenant = await session.get(Tenant, credential.tenant_id)
    if tenant is None or tenant.status != TenantStatus.ACTIVE:
        return None

    await _record_last_used(credential.id, now)
    return credential
