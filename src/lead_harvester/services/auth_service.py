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

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.auth import ServiceCredential, ServiceRole
from lead_harvester.models.tenancy import DEFAULT_TENANT_ID


def hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def generate_raw_token() -> str:
    return secrets.token_urlsafe(32)


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
    """
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


async def authenticate_token(session: AsyncSession, raw_token: str) -> ServiceCredential | None:
    """
    Returns the matching credential if it exists, is not revoked, and has
    not expired -- None otherwise. A successful match updates
    last_used_at. Never raises for an unknown/invalid token; the caller
    (api/dependencies.py::get_current_user) turns a None result into a 401.
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

    credential.last_used_at = now
    return credential
