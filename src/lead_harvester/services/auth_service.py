"""
Issues, authenticates, and revokes ServiceCredential rows -- see
models/auth.py's module docstring for why this replaces the previous
hardcoded bearer tokens in api/dependencies.py.
"""

from __future__ import annotations

import asyncio
import datetime as dt
import hashlib
import secrets
import uuid

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.database import get_session
from lead_harvester.models.auth import ServiceCredential, ServiceRole
from lead_harvester.models.tenancy import DEFAULT_TENANT_ID, Tenant, TenantStatus

# Keeps a strong reference to every in-flight _drain_last_used_writes
# task -- asyncio only holds a weak reference to a task once nothing else
# does, so a fire-and-forget create_task() with no reference kept
# anywhere can be garbage-collected mid-await, silently dropping the
# write. Discarded from this set via its own done callback once it finishes.
_pending_last_used_writes: set[asyncio.Task] = set()

# Coalescing state for _schedule_last_used_write: at most one writer task
# per credential_id at a time, however many requests authenticate with
# that credential in a burst -- see _schedule_last_used_write's docstring.
# _pending_last_used_timestamps holds the latest not-yet-written `when`
# per credential_id; _in_flight_last_used_writers marks which credential_ids
# currently have a _drain_last_used_writes task running.
_pending_last_used_timestamps: dict[uuid.UUID, dt.datetime] = {}
_in_flight_last_used_writers: set[uuid.UUID] = set()


def hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def generate_raw_token() -> str:
    return secrets.token_urlsafe(32)


class TenantNotFoundError(ValueError):
    """Raised by issue_service_credential() when tenant_id matches no Tenant row."""


class CredentialNameInUseError(ValueError):
    """Raised by issue_service_credential() when `name` already has an active (non-revoked) credential."""


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
    unhandled IntegrityError instead of a clean, catchable error. Raises
    CredentialNameInUseError if `name` already has an active credential --
    same reasoning, but for the partial unique index
    (uq_service_credentials_active_name) rather than a foreign key.
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

    # Transaction-scoped advisory lock on `name`, held until this
    # transaction commits or rolls back -- the read-then-insert below is
    # otherwise a TOCTOU race: two concurrent issuances for the same name
    # can both pass this "no active credential" check before either
    # commits, and one would fail with a raw IntegrityError against
    # uq_service_credentials_active_name instead of a clean
    # CredentialNameInUseError. Same pattern as
    # tenant_config_service.set_tenant_config's lock.
    # pg_advisory_xact_lock has no single-int4 overload (only bigint, or
    # two int4s) -- a fixed domain-separation string as the first key
    # keeps this lock namespace distinct from other hashtext(...)-keyed
    # locks in this codebase (e.g. tenant_config_service's) that hash two
    # real values instead of one.
    await session.execute(
        select(
            func.pg_advisory_xact_lock(
                func.hashtext("service_credential_name"), func.hashtext(name)
            )
        )
    )

    existing = (
        await session.scalars(
            select(ServiceCredential).where(
                ServiceCredential.name == name, ServiceCredential.revoked_at.is_(None)
            )
        )
    ).first()
    if existing is not None:
        raise CredentialNameInUseError(
            f"{name!r} already has an active credential -- revoke it first "
            "(revoke-service-credential), or choose a different name."
        )

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
    # Filtering to revoked_at IS NULL (not just matching by name) matters
    # once a name has been reissued (see the partial unique index in
    # models/auth.py): an unfiltered, unordered query could return the
    # old revoked row instead of the active replacement, wrongly
    # reporting "not found" here and leaving the real active credential
    # unrevoked.
    credential = (
        await session.scalars(
            select(ServiceCredential).where(
                ServiceCredential.name == name, ServiceCredential.revoked_at.is_(None)
            )
        )
    ).first()
    if credential is None:
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

    Never call this directly from authenticate_token() -- see
    _schedule_last_used_write().
    """
    async with get_session() as session:
        await session.execute(
            update(ServiceCredential)
            .where(
                ServiceCredential.id == credential_id,
                # Concurrent requests on the same token schedule these
                # writes out of order -- without this guard, a slower
                # request's older `when` could land after a faster
                # request's newer one and move last_used_at backward.
                # Keeps the column monotonic instead of just "most
                # recently written".
                (ServiceCredential.last_used_at.is_(None))
                | (ServiceCredential.last_used_at < when),
            )
            .values(last_used_at=when)
            # This update runs against a different session than the one
            # that loaded `credential` in authenticate_token() -- there is
            # no in-memory ORM object here for SQLAlchemy to reconcile
            # against, so ask for the plain, predictable bulk-UPDATE
            # behavior rather than the "evaluate"/"fetch" auto-sync
            # strategies meant for same-session in-memory consistency.
            .execution_options(synchronize_session=False)
        )


async def _drain_last_used_writes(credential_id: uuid.UUID) -> None:
    """
    Writes _pending_last_used_timestamps[credential_id] and loops rather
    than returning immediately, in case a newer timestamp for the SAME
    credential_id was coalesced in (see _schedule_last_used_write) while
    this write was in flight -- that timestamp needs a writer too, and by
    looping here instead of spawning another task for it, at most one
    writer (one task, one transaction) is ever in flight per credential_id,
    however many requests authenticate with it in a burst. Runs unawaited
    by the caller -- an exception here has nowhere to propagate to, so it
    must be swallowed explicitly rather than surface as an "exception was
    never retrieved" warning from a task nobody is watching. last_used_at
    is observability data, not a correctness-critical write; losing one
    occasionally is an acceptable trade for never blocking or failing the
    request it came from.
    """
    try:
        while True:
            when = _pending_last_used_timestamps.pop(credential_id, None)
            if when is None:
                return
            await _record_last_used(credential_id, when)
    except Exception as e:
        print(f"[auth] Failed to record last_used_at for credential {credential_id}: {e}")
    finally:
        _in_flight_last_used_writers.discard(credential_id)


def _schedule_last_used_write(credential_id: uuid.UUID, when: dt.datetime) -> None:
    """
    Records `when` as the latest last_used_at to write for credential_id,
    and ensures exactly one _drain_last_used_writes task is running for it
    -- never a second one. Without this coalescing, a sustained burst of
    requests on one shared credential would spawn one task and one
    database transaction per request, with no bound: thousands of
    pool-waiting tasks competing with real request traffic for
    connections. Coalescing to "one writer per credential_id, always
    writing the newest known timestamp" keeps the in-flight count bounded
    by the number of distinct credentials in use, not the request rate.

    Also avoids a second pool checkout on the caller's own connection:
    authenticate_token()'s caller (api/dependencies.py::get_current_user)
    already holds one pooled connection via its own session argument --
    awaiting a second get_session() checkout inline, here, would mean
    every concurrent authenticated request holds two pool connections at
    once. Under a burst that fills the pool, every request's outer
    connection is then stuck waiting for a second connection that's
    itself held by another request stuck the same way -- nothing left to
    release one, so authentication stalls until pool timeout. Not
    awaiting this task means authenticate_token() returns as soon as its
    own (single) query finishes; the writer task acquires its connection
    whenever the pool actually has room, independent of the request's
    lifecycle.
    """
    existing = _pending_last_used_timestamps.get(credential_id)
    if existing is None or when > existing:
        _pending_last_used_timestamps[credential_id] = when

    if credential_id in _in_flight_last_used_writers:
        # A writer for this credential is already running (or about to
        # loop again) -- it will pick up the timestamp just stored above.
        # No new task needed.
        return

    _in_flight_last_used_writers.add(credential_id)
    task = asyncio.create_task(_drain_last_used_writes(credential_id))
    _pending_last_used_writes.add(task)
    task.add_done_callback(_pending_last_used_writes.discard)


async def wait_for_pending_last_used_writes() -> None:
    """
    Test-only hook: awaits every last_used_at write _schedule_last_used_write
    has fired but not yet completed. Production code never needs this --
    the entire point of scheduling rather than awaiting is that nothing
    in the request path depends on these finishing.
    """
    pending = list(_pending_last_used_writes)
    if pending:
        await asyncio.gather(*pending)


async def authenticate_token(session: AsyncSession, raw_token: str) -> ServiceCredential | None:
    """
    Returns the matching credential if it exists, is not revoked, has not
    expired, and belongs to an ACTIVE tenant -- None otherwise. A
    successful match schedules (but does not wait for) a last_used_at
    write on a separate connection (see _schedule_last_used_write) -- the
    returned object's own last_used_at attribute reflects its state as
    loaded, i.e. from before this call, and the durable write may not
    have landed yet by the time this function returns. Never raises for
    an unknown/invalid token; the caller
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

    # A credential is only as trustworthy as its tenant -- suspending a
    # tenant must terminate every one of its credentials' access
    # immediately, without requiring each one to be individually revoked.
    tenant = await session.get(Tenant, credential.tenant_id)
    if tenant is None or tenant.status != TenantStatus.ACTIVE:
        return None

    _schedule_last_used_write(credential.id, now)
    return credential
