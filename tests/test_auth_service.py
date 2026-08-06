import contextlib
import datetime as dt
import uuid
from unittest.mock import patch

import pytest

from lead_harvester.models.auth import ServiceRole
from lead_harvester.models.tenancy import DEFAULT_TENANT_ID
from lead_harvester.services.auth_service import (
    TenantScopeIncompleteError,
    authenticate_token,
    generate_raw_token,
    hash_token,
    issue_service_credential,
    revoke_service_credential,
)


@contextlib.asynccontextmanager
async def _fake_get_session(session):
    yield session


def _route_last_used_writes_to(db_session):
    # authenticate_token() records last_used_at on its own independent
    # session (see auth_service.py::_record_last_used) so the write
    # survives a later rollback in the caller's transaction -- that
    # independent session normally comes from database.py's get_session(),
    # bound to DATABASE_URL. Tests run against TEST_DATABASE_URL instead,
    # so a successful authenticate_token() call must redirect that write
    # to db_session, the same way api/dependencies.py's own tests redirect
    # require_permission()'s audit write.
    return patch(
        "lead_harvester.services.auth_service.get_session",
        new=lambda: _fake_get_session(db_session),
    )


def test_hash_token_is_deterministic_and_never_equals_the_raw_token():
    raw = "a-raw-token-value"
    assert hash_token(raw) == hash_token(raw)
    assert hash_token(raw) != raw


def test_generate_raw_token_produces_distinct_high_entropy_values():
    tokens = {generate_raw_token() for _ in range(20)}
    assert len(tokens) == 20
    assert all(len(t) >= 32 for t in tokens)


@pytest.mark.asyncio
async def test_issue_then_authenticate_round_trip(db_session):
    credential, raw_token = await issue_service_credential(
        db_session, name="test-admin", role=ServiceRole.ADMIN
    )
    await db_session.commit()

    with _route_last_used_writes_to(db_session):
        authenticated = await authenticate_token(db_session, raw_token)

    assert authenticated is not None
    assert authenticated.id == credential.id
    assert authenticated.role == ServiceRole.ADMIN

    # last_used_at is recorded on a separate row by _record_last_used --
    # `authenticated` itself (loaded before that write) won't reflect it.
    await db_session.refresh(credential)
    assert credential.last_used_at is not None


@pytest.mark.asyncio
async def test_issue_never_persists_the_raw_token(db_session):
    _credential, raw_token = await issue_service_credential(
        db_session, name="test-no-raw-storage", role=ServiceRole.VIEWER
    )
    await db_session.commit()

    # The stored hash must not simply be the raw token -- confirms the
    # credential row itself never carries the plaintext value anywhere.
    with _route_last_used_writes_to(db_session):
        authenticated = await authenticate_token(db_session, raw_token)
    assert authenticated is not None
    assert authenticated.token_hash != raw_token


@pytest.mark.asyncio
async def test_authenticate_rejects_unknown_token(db_session):
    assert await authenticate_token(db_session, "never-issued-token") is None


@pytest.mark.asyncio
async def test_authenticate_rejects_revoked_credential(db_session):
    _credential, raw_token = await issue_service_credential(
        db_session, name="test-revoked", role=ServiceRole.REVIEWER
    )
    await db_session.commit()

    revoked = await revoke_service_credential(db_session, "test-revoked")
    await db_session.commit()

    assert revoked is not None
    assert revoked.revoked_at is not None
    assert await authenticate_token(db_session, raw_token) is None


@pytest.mark.asyncio
async def test_authenticate_rejects_expired_credential(db_session):
    expired_at = dt.datetime.now(dt.UTC) - dt.timedelta(seconds=1)
    _credential, raw_token = await issue_service_credential(
        db_session, name="test-expired", role=ServiceRole.ADMIN, expires_at=expired_at
    )
    await db_session.commit()

    assert await authenticate_token(db_session, raw_token) is None


@pytest.mark.asyncio
async def test_authenticate_accepts_credential_with_future_expiry(db_session):
    future = dt.datetime.now(dt.UTC) + dt.timedelta(days=1)
    _credential, raw_token = await issue_service_credential(
        db_session, name="test-future-expiry", role=ServiceRole.ADMIN, expires_at=future
    )
    await db_session.commit()

    with _route_last_used_writes_to(db_session):
        assert await authenticate_token(db_session, raw_token) is not None


@pytest.mark.asyncio
async def test_revoke_returns_none_for_unknown_name(db_session):
    assert await revoke_service_credential(db_session, "does-not-exist") is None


@pytest.mark.asyncio
async def test_revoke_returns_none_when_already_revoked(db_session):
    await issue_service_credential(db_session, name="test-double-revoke", role=ServiceRole.ADMIN)
    await db_session.commit()

    first = await revoke_service_credential(db_session, "test-double-revoke")
    await db_session.commit()
    second = await revoke_service_credential(db_session, "test-double-revoke")

    assert first is not None
    assert second is None


@pytest.mark.asyncio
async def test_issue_rejects_a_non_default_tenant_id(db_session):
    # Only CanonicalInstitution/Branch/ContactPoint and InstitutionService's
    # reads are tenant-scoped so far -- a credential for any other tenant
    # would see every other tenant's data through every unscoped route.
    with pytest.raises(TenantScopeIncompleteError):
        await issue_service_credential(
            db_session, name="test-other-tenant", role=ServiceRole.ADMIN, tenant_id=uuid.uuid4()
        )


@pytest.mark.asyncio
async def test_issue_allows_reusing_a_name_after_the_prior_credential_is_revoked(db_session):
    # cli.py's issue-service-credential docstring tells operators to
    # rerun the command under the same --name to replace a lost token --
    # that only works if a revoked (not deleted) predecessor doesn't
    # permanently hold the name.
    await issue_service_credential(db_session, name="test-reissue", role=ServiceRole.ADMIN)
    await db_session.commit()
    await revoke_service_credential(db_session, "test-reissue")
    await db_session.commit()

    new_credential, _raw_token = await issue_service_credential(
        db_session, name="test-reissue", role=ServiceRole.ADMIN
    )

    assert new_credential.name == "test-reissue"
    assert new_credential.revoked_at is None


@pytest.mark.asyncio
async def test_issue_rejects_reusing_a_name_still_active(db_session):
    await issue_service_credential(db_session, name="test-still-active", role=ServiceRole.ADMIN)
    await db_session.flush()

    with pytest.raises(Exception):  # noqa: B017 -- asserting the DB-level unique violation
        await issue_service_credential(db_session, name="test-still-active", role=ServiceRole.ADMIN)
        await db_session.flush()


@pytest.mark.asyncio
async def test_authenticate_rejects_a_credential_whose_tenant_is_suspended(db_session):
    # Suspending a tenant must terminate every one of its credentials'
    # access immediately -- without this check, suspension would require
    # individually revoking every credential that tenant ever issued.
    # Uses the default tenant itself (issue_service_credential refuses any
    # other tenant_id -- see TenantScopeIncompleteError) and restores its
    # status afterward since it's shared, session-scoped seed data other
    # tests also rely on being ACTIVE.
    from sqlalchemy import select

    from lead_harvester.models.tenancy import Tenant, TenantStatus

    _credential, raw_token = await issue_service_credential(
        db_session, name="test-suspended-tenant", role=ServiceRole.ADMIN
    )
    await db_session.commit()

    with _route_last_used_writes_to(db_session):
        assert await authenticate_token(db_session, raw_token) is not None

    default_tenant = (
        await db_session.scalars(select(Tenant).where(Tenant.id == DEFAULT_TENANT_ID))
    ).one()
    default_tenant.status = TenantStatus.SUSPENDED
    await db_session.flush()
    try:
        assert await authenticate_token(db_session, raw_token) is None
    finally:
        default_tenant.status = TenantStatus.ACTIVE
        await db_session.flush()


@pytest.mark.asyncio
async def test_issue_rejects_a_tenant_id_matching_no_tenant_row(db_session):
    # A mistyped, stale, or not-yet-migrated tenant must raise a clean,
    # catchable error at this boundary rather than reach the tenant_id
    # foreign key and surface as an unhandled IntegrityError. Deletes the
    # seeded default tenant row within this test's own savepoint (rolled
    # back afterward, so it doesn't affect any other test) to exercise
    # the "tenant_id matches no row" path -- DEFAULT_TENANT_ID is the
    # only tenant_id issue_service_credential accepts at all right now
    # (see TenantScopeIncompleteError), so it's also the only one this
    # check can realistically ever see.
    from sqlalchemy import delete

    from lead_harvester.models.tenancy import Tenant
    from lead_harvester.services.auth_service import TenantNotFoundError

    await db_session.execute(delete(Tenant).where(Tenant.id == DEFAULT_TENANT_ID))
    await db_session.flush()

    with pytest.raises(TenantNotFoundError):
        await issue_service_credential(
            db_session, name="test-no-tenant-row", role=ServiceRole.ADMIN
        )


@pytest.mark.asyncio
async def test_issue_accepts_the_default_tenant_id_explicitly(db_session):
    credential, _raw_token = await issue_service_credential(
        db_session,
        name="test-explicit-default-tenant",
        role=ServiceRole.ADMIN,
        tenant_id=DEFAULT_TENANT_ID,
    )
    assert credential.tenant_id == DEFAULT_TENANT_ID
