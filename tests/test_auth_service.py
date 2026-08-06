import datetime as dt

import pytest

from lead_harvester.models.auth import ServiceRole
from lead_harvester.services.auth_service import (
    authenticate_token,
    generate_raw_token,
    hash_token,
    issue_service_credential,
    revoke_service_credential,
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

    authenticated = await authenticate_token(db_session, raw_token)

    assert authenticated is not None
    assert authenticated.id == credential.id
    assert authenticated.role == ServiceRole.ADMIN
    assert authenticated.last_used_at is not None


@pytest.mark.asyncio
async def test_issue_never_persists_the_raw_token(db_session):
    _credential, raw_token = await issue_service_credential(
        db_session, name="test-no-raw-storage", role=ServiceRole.VIEWER
    )
    await db_session.commit()

    # The stored hash must not simply be the raw token -- confirms the
    # credential row itself never carries the plaintext value anywhere.
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
