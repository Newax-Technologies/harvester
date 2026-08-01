import pytest

from lead_harvester.api.dependencies import User
from lead_harvester.api.errors import AuthorizationError
from lead_harvester.api.permissions import (
    ROLE_PERMISSIONS,
    Permission,
    require_permission,
    role_has_permission,
)


def test_admin_holds_every_permission():
    assert ROLE_PERMISSIONS["admin"] == frozenset(Permission)


def test_viewer_holds_only_read_permissions():
    assert ROLE_PERMISSIONS["viewer"] == {
        Permission.LEADS_READ,
        Permission.COMPLIANCE_READ,
        Permission.OPERATIONS_READ,
    }


def test_unknown_role_holds_no_permissions():
    assert role_has_permission("nonexistent-role", Permission.LEADS_READ) is False


def test_role_has_permission_matches_the_matrix():
    assert role_has_permission("reviewer", Permission.LEADS_CREATE) is True
    assert role_has_permission("reviewer", Permission.SECTORS_MANAGE) is False


@pytest.mark.asyncio
async def test_require_permission_returns_the_user_when_permitted():
    checker = require_permission(Permission.LEADS_READ)
    user = User(id="u1", username="viewer-user", role="viewer")

    result = await checker(current_user=user)

    assert result is user


@pytest.mark.asyncio
async def test_require_permission_raises_when_not_permitted():
    checker = require_permission(Permission.SECTORS_MANAGE)
    user = User(id="u1", username="viewer-user", role="viewer")

    with pytest.raises(AuthorizationError):
        await checker(current_user=user)
