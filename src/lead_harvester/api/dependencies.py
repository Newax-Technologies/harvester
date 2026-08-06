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


def require_permission(permission: str):
    """
    Deny-by-default permission dependency (see authz.py's PERMISSIONS
    catalog). A denial is audited on its own, immediately-committed
    session -- the main request's session/transaction is about to be
    rolled back by AuthorizationError propagating through get_session(),
    which would silently discard the audit row too if it shared that
    session.
    """

    async def permission_checker(current_user: User = Depends(get_current_user)) -> User:
        if not is_permitted(permission, current_user.role):
            async with get_session() as audit_session:
                audit_session.add(
                    AuditLog(
                        action="authorization.denied",
                        actor=current_user.username,
                        entity_type="Permission",
                        entity_id=_NO_ENTITY,
                        new_state={"permission": permission, "role": current_user.role},
                    )
                )
            raise AuthorizationError()
        return current_user

    return permission_checker


_lead_sync_emitter = LeadSyncEmitter(settings)


def get_lead_sync_emitter() -> LeadSyncEmitter:
    """Dependency to get the lead sync webhook emitter (overridable in tests)."""
    return _lead_sync_emitter
