import os

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.errors import AuthenticationError, AuthorizationError
from lead_harvester.config import settings
from lead_harvester.database import get_session
from lead_harvester.integrations.lead_sync_emitter import LeadSyncEmitter

security = HTTPBearer(auto_error=False)


class User:
    def __init__(self, id: str, username: str, role: str):
        self.id = id
        self.username = username
        self.role = role


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """
    Dependency to get the current authenticated user.
    For local development, DEV_AUTH_ENABLED can bypass strict token checks.
    """
    dev_auth = os.getenv("DEV_AUTH_ENABLED", "false").lower() == "true"

    if dev_auth:
        return User(
            id="usr_dev_admin", username=os.getenv("DEV_AUTH_USER", "local-admin"), role="admin"
        )

    if not credentials:
        raise AuthenticationError()

    # Mocking real JWT check for now
    token = credentials.credentials
    if token == "secret-admin-token":
        return User(id="usr_admin", username="admin-user", role="admin")
    elif token == "secret-reviewer-token":
        return User(id="usr_reviewer", username="reviewer-user", role="reviewer")
    else:
        # Default fallback if token is passed but unknown could be a viewer
        return User(id="usr_viewer", username="viewer-user", role="viewer")


def require_roles(*roles: str):
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise AuthorizationError()
        return current_user

    return role_checker


async def get_db_session() -> AsyncSession:
    """Dependency to get the database session"""
    async with get_session() as session:
        yield session


_lead_sync_emitter = LeadSyncEmitter(settings)


def get_lead_sync_emitter() -> LeadSyncEmitter:
    """Dependency to get the lead sync webhook emitter (overridable in tests)."""
    return _lead_sync_emitter
