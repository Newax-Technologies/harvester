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


# Keeps a strong reference to every in-flight _drain_denial_audits task --
# see services/auth_service.py's identical _pending_last_used_writes for why.
_pending_denial_audits: set[asyncio.Task] = set()

# Rows not yet written, and whether a drain task is currently running for
# them -- see _schedule_denial_audit's docstring. Unlike last_used_at
# (where only the newest value per credential matters, so coalescing can
# just overwrite), every denial is its own audit record worth keeping;
# these accumulate into one row list instead.
_pending_denial_audit_rows: list[AuditLog] = []
_denial_audit_writer_running = False

# Caps _pending_denial_audit_rows so a sustained burst of denials from one
# credential can't grow this list -- and the memory it holds -- without
# bound while a write is in flight. A row beyond this cap is dropped, not
# queued; denial audits are best-effort observability, not a durability
# guarantee (see the docstring below).
_MAX_PENDING_DENIAL_AUDIT_ROWS = 1000


async def _drain_denial_audits() -> None:
    """
    Writes every row in _pending_denial_audit_rows in one batched
    transaction, and loops if more arrived while that write was in
    flight -- the same single-writer-per-burst shape as
    auth_service.py's _drain_last_used_writes, applied to a list of rows
    instead of "the newest value per key", since every denial is its own
    record worth keeping rather than one that supersedes the last. Caps
    concurrent writer tasks/transactions at one, however many denials
    happen concurrently -- one task and one transaction per *request*
    (the previous shape) had no such bound, so a burst of forbidden
    calls from a single valid-but-low-privilege credential could grow
    both memory (unbounded pending tasks) and pool contention (unbounded
    concurrent transactions) without limit. Runs unawaited by the
    caller -- an exception here has nowhere to propagate to, so it must
    be swallowed explicitly. Denial audits are observability data, not a
    correctness-critical write; losing a batch to a transient DB error
    is an acceptable trade for never blocking or deadlocking the
    request that triggered it.
    """
    global _denial_audit_writer_running
    try:
        while _pending_denial_audit_rows:
            batch = _pending_denial_audit_rows[:]
            _pending_denial_audit_rows.clear()
            try:
                async with get_session() as session:
                    session.add_all(batch)
            except Exception as e:
                print(f"[authz] Failed to write a denial-audit batch of {len(batch)}: {e}")
    finally:
        _denial_audit_writer_running = False


def _schedule_denial_audit(actor: str, permission: str, role: str) -> None:
    """
    Queues a denial-audit row and ensures exactly one _drain_denial_audits
    task is running to write it -- never a second one, and never a new
    task per request. See _drain_denial_audits' docstring for why.
    """
    global _denial_audit_writer_running
    if len(_pending_denial_audit_rows) >= _MAX_PENDING_DENIAL_AUDIT_ROWS:
        print(
            f"[authz] Denial-audit queue full ({_MAX_PENDING_DENIAL_AUDIT_ROWS}) -- "
            f"dropping a denial-audit row for {actor!r}."
        )
        return

    _pending_denial_audit_rows.append(
        AuditLog(
            action="authorization.denied",
            actor=actor,
            entity_type="Permission",
            entity_id=_NO_ENTITY,
            new_state={"permission": permission, "role": role},
        )
    )

    if _denial_audit_writer_running:
        # A writer is already running (or about to loop again) -- it will
        # pick up the row just appended above. No new task needed.
        return

    _denial_audit_writer_running = True
    task = asyncio.create_task(_drain_denial_audits())
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
