import contextlib
from unittest.mock import patch

import pytest
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import select

from lead_harvester.api.dependencies import User, get_current_user, require_permission
from lead_harvester.api.errors import AuthenticationError, AuthorizationError
from lead_harvester.config import settings
from lead_harvester.models.audit import AuditLog
from lead_harvester.models.auth import ServiceRole
from lead_harvester.services.auth_service import (
    issue_service_credential,
    revoke_service_credential,
)


def _bearer(token: str) -> HTTPAuthorizationCredentials:
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)


@contextlib.asynccontextmanager
async def _fake_get_session(session):
    yield session


@pytest.mark.asyncio
async def test_get_current_user_accepts_a_valid_issued_token(db_session):
    _credential, raw_token = await issue_service_credential(
        db_session, name="dep-test-reviewer", role=ServiceRole.REVIEWER
    )
    await db_session.commit()

    # authenticate_token() (called by get_current_user) records
    # last_used_at on its own independent session bound to DATABASE_URL --
    # redirect that to db_session, same as the audit-write tests below.
    with patch(
        "lead_harvester.services.auth_service.get_session",
        new=lambda: _fake_get_session(db_session),
    ):
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


@pytest.mark.asyncio
async def test_require_permission_allows_a_permitted_role():
    checker = require_permission("drafts.decide")
    user = User(id="u1", username="rev", role="reviewer")

    result = await checker(current_user=user)

    assert result is user


@pytest.mark.asyncio
async def test_require_permission_denies_and_audits_an_unpermitted_role(db_session):
    checker = require_permission("drafts.decide")
    user = User(id="u2", username="a-viewer", role="viewer")

    with (
        patch(
            "lead_harvester.api.dependencies.get_session", new=lambda: _fake_get_session(db_session)
        ),
        pytest.raises(AuthorizationError),
    ):
        await checker(current_user=user)

    audit_rows = (
        (
            await db_session.execute(
                select(AuditLog).where(AuditLog.action == "authorization.denied")
            )
        )
        .scalars()
        .all()
    )
    assert any(
        row.actor == "a-viewer" and row.new_state.get("permission") == "drafts.decide"
        for row in audit_rows
    )


@pytest.mark.asyncio
async def test_require_permission_denies_unregistered_permission_by_default(db_session):
    checker = require_permission("not_a_real_permission")
    user = User(id="u3", username="admin-user", role="admin")

    with (
        patch(
            "lead_harvester.api.dependencies.get_session", new=lambda: _fake_get_session(db_session)
        ),
        pytest.raises(AuthorizationError),
    ):
        await checker(current_user=user)


@pytest.mark.asyncio
async def test_require_permission_truncates_a_long_username_for_the_audit_actor_column(
    db_session,
):
    # ServiceCredential.name allows up to 255 characters but AuditLog.actor
    # is String(100) -- a long credential name must still get a clean
    # AuthorizationError, not an IntegrityError from the audit write.
    checker = require_permission("drafts.decide")
    long_username = "a" * 255
    user = User(id="u4", username=long_username, role="viewer")

    with (
        patch(
            "lead_harvester.api.dependencies.get_session", new=lambda: _fake_get_session(db_session)
        ),
        pytest.raises(AuthorizationError),
    ):
        await checker(current_user=user)

    audit_rows = (
        (
            await db_session.execute(
                select(AuditLog).where(AuditLog.action == "authorization.denied")
            )
        )
        .scalars()
        .all()
    )
    assert any(row.actor == long_username[:100] for row in audit_rows)
