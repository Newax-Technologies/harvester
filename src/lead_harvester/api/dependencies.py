from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.errors import AuthenticationError, AuthorizationError
from lead_harvester.config import settings
from lead_harvester.database import get_session
from lead_harvester.integrations.lead_sync_emitter import LeadSyncEmitter
from lead_harvester.services.auth_service import authenticate_token

security = HTTPBearer(auto_error=False)


class User:
    def __init__(self, id: str, username: str, role: str):
        self.id = id
        self.username = username
        self.role = role


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
        return User(id="usr_dev_admin", username=settings.dev_auth_user, role="admin")

    if not credentials:
        raise AuthenticationError()

    credential = await authenticate_token(session, credentials.credentials)
    if credential is None:
        raise AuthenticationError()

    return User(id=str(credential.id), username=credential.name, role=credential.role.value)


def require_roles(*roles: str):
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise AuthorizationError()
        return current_user

    return role_checker


_lead_sync_emitter = LeadSyncEmitter(settings)


def get_lead_sync_emitter() -> LeadSyncEmitter:
    """Dependency to get the lead sync webhook emitter (overridable in tests)."""
    return _lead_sync_emitter
