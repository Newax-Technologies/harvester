import asyncio
import uuid

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.errors import AuthenticationError, AuthorizationError
from lead_harvester.authz import is_permitted
from lead_harvester.config import settings
from lead_harvester.database import get_session
from lead_harvester.integrations.lead_sync_emitter import LeadSyncEmitter
from lead_harvester.models.audit import AuditLog
from lead_harvester.models.tenancy import DEFAULT_TENANT_ID
from lead_harvester.services.auth_service import authenticate_token

security = HTTPBearer(auto_error=False)

# entity_id is NOT NULL on AuditLog, but a denied permission check often
# has no single resource in scope (e.g. a list endpoint) -- the nil UUID
# marks "no specific entity"; the permission/role context lives in
# new_state instead. See require_permission() below.
_NO_ENTITY = uuid.UUID(int=0)


class User:
    def __init__(self, id: str, username: str, role: str, tenant_id: uuid.UUID = DEFAULT_TENANT_ID):
        self.id = id
        self.username = username
        self.role = role
        self.tenant_id = tenant_id


async def get_db_session() -> AsyncSession:
    """Dependency to get the database session"""
    async with get_session() as session:
        yield session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    """
    Dependency to get the current authenticated user. Bearer tokens are
    matched against ServiceCredential (models/auth.py) -- an unrecognized,
    revoked, or expired token is rejected outright, not silently treated
    as a valid low-privilege viewer (see models/auth.py's module docstring
    for why that fallback existed and had to go).

    For local development, Settings.dev_auth_enabled can bypass credential
    checks -- Settings itself refuses to allow that in production.
    """
    if settings.dev_auth_enabled:
        return User(
            id="usr_dev_admin",
            username=settings.dev_auth_user,
            role="admin",
            tenant_id=DEFAULT_TENANT_ID,
        )

    if not credentials:
        raise AuthenticationError()

    credential = await authenticate_token(session, credentials.credentials)
    if credential is None:
        raise AuthenticationError()

    return User(
        id=str(credential.id),
        username=credential.name,
        role=credential.role.value,
        tenant_id=credential.tenant_id,
    )


_pending_denial_audits: set[asyncio.Task] = set()


async def _write_denial_audit(actor: str, permission: str, role: str) -> None:
    async with get_session() as session:
        session.add(
            AuditLog(
                action="authorization.denied",
                actor=actor,
                entity_type="Permission",
                entity_id=_NO_ENTITY,
                new_state={"permission": permission, "role": role},
            )
        )


async def _write_denial_audit_ignoring_errors(actor: str, permission: str, role: str) -> None:
    # Runs unawaited (see _schedule_denial_audit) -- an exception here has
    # nowhere to propagate to, so it must be swallowed explicitly. The 403
    # already returned to the caller by the time this runs; losing an
    # occasional denial-audit row to a transient DB error is an acceptable
    # trade for never blocking or deadlocking the request that triggered it.
    try:
        await _write_denial_audit(actor, permission, role)
    except Exception as e:
        print(f"[authz] Failed to write denial audit for {actor!r}: {e}")


def _schedule_denial_audit(actor: str, permission: str, role: str) -> None:
    task = asyncio.create_task(_write_denial_audit_ignoring_errors(actor, permission, role))
    _pending_denial_audits.add(task)
    task.add_done_callback(_pending_denial_audits.discard)


async def wait_for_pending_denial_audits() -> None:
    """Test-only hook -- see services/auth_service.py's wait_for_pending_last_used_writes."""
    pending = list(_pending_denial_audits)
    if pending:
        await asyncio.gather(*pending)


def require_permission(permission: str):
    """
    Deny-by-default permission dependency (see authz.py's PERMISSIONS
    catalog). A denial is audited fire-and-forget, on its own session --
    the main request's get_db_session dependency is already checked out
    for the whole request by this point (get_current_user depends on it),
    so awaiting a second get_session() here would hold two pool
    connections per denied request; under a burst that fills the pool,
    every request could end up waiting on a connection nothing is free to
    release. See services/auth_service.py's _schedule_last_used_write for
    the same pattern and reasoning.
    """

    async def permission_checker(current_user: User = Depends(get_current_user)) -> User:
        if not is_permitted(permission, current_user.role):
            # ServiceCredential.name allows up to 255 characters but
            # AuditLog.actor is only String(100).
            _schedule_denial_audit(current_user.username[:100], permission, current_user.role)
            raise AuthorizationError()
        return current_user

    return permission_checker


_lead_sync_emitter = LeadSyncEmitter(settings)


def get_lead_sync_emitter() -> LeadSyncEmitter:
    """Dependency to get the lead sync webhook emitter (overridable in tests)."""
    return _lead_sync_emitter
