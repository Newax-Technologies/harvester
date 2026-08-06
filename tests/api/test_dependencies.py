import pytest
from fastapi.security import HTTPAuthorizationCredentials

from lead_harvester.api.dependencies import get_current_user
from lead_harvester.api.errors import AuthenticationError
from lead_harvester.config import settings
from lead_harvester.models.auth import ServiceRole
from lead_harvester.services.auth_service import (
    issue_service_credential,
    revoke_service_credential,
)


def _bearer(token: str) -> HTTPAuthorizationCredentials:
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)


@pytest.mark.asyncio
async def test_get_current_user_accepts_a_valid_issued_token(db_session):
    _credential, raw_token = await issue_service_credential(
        db_session, name="dep-test-reviewer", role=ServiceRole.REVIEWER
    )
    await db_session.commit()

    user = await get_current_user(credentials=_bearer(raw_token), session=db_session)

    assert user.username == "dep-test-reviewer"
    assert user.role == "reviewer"


@pytest.mark.asyncio
async def test_get_current_user_rejects_an_unrecognized_token(db_session):
    # Previously any unrecognized-but-present token silently authenticated
    # as a viewer -- an unknown bearer token must now be rejected outright.
    with pytest.raises(AuthenticationError):
        await get_current_user(credentials=_bearer("nobody-ever-issued-this"), session=db_session)


@pytest.mark.asyncio
async def test_get_current_user_rejects_missing_credentials(db_session):
    with pytest.raises(AuthenticationError):
        await get_current_user(credentials=None, session=db_session)


@pytest.mark.asyncio
async def test_get_current_user_rejects_a_revoked_token(db_session):
    _credential, raw_token = await issue_service_credential(
        db_session, name="dep-test-revoked", role=ServiceRole.ADMIN
    )
    await db_session.commit()
    await revoke_service_credential(db_session, "dep-test-revoked")
    await db_session.commit()

    with pytest.raises(AuthenticationError):
        await get_current_user(credentials=_bearer(raw_token), session=db_session)


@pytest.mark.asyncio
async def test_get_current_user_dev_bypass_short_circuits_before_any_token_check(
    db_session, monkeypatch
):
    monkeypatch.setattr(settings, "dev_auth_enabled", True)
    monkeypatch.setattr(settings, "dev_auth_user", "local-admin")

    user = await get_current_user(credentials=None, session=db_session)

    assert user.username == "local-admin"
    assert user.role == "admin"
