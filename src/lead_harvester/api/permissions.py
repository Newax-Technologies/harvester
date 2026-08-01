"""
Explicit permission matrix -- every route in the domains listed below must
enforce the specific permission relevant to what it does, not just "is
logged in" (`get_current_user` alone) or the coarser 3-role check
(`require_roles`) `drafts.py`/`resolution_reviews.py` already use.

`Permission` is the exhaustive, named list of server-side-enforced
actions across these API domains: lead profiles, lead export, manual
lead creation, sector configuration, daily selection, compliance
(suppressions + deletion requests), deletion fulfillment specifically
(deliberately split from the rest of compliance -- it's the one action
that's actually irreversible, see `services/compliance_service.py::fulfill_deletion`'s
own docstring), event outbox administration, operations visibility, and
audit log visibility.

`ROLE_PERMISSIONS` is the matrix itself: which of the three existing
roles (`api/dependencies.py::User.role` -- admin/reviewer/viewer) holds
which permissions. `admin` holds every permission. `reviewer` holds the
day-to-day pipeline-work permissions (read/create leads, run daily
selection, see compliance state and operational health) but not the
more sensitive/destructive ones (bulk PII export, sector config,
suppression/deletion-request writes, deletion fulfillment, outbox
retries, audit log). `viewer` holds only read permissions, and not
even all of those (no audit log). This mapping is a deliberate design
choice, not dictated by any existing spec -- adjust the matrix below if
the actual intended split differs.

`require_permission(Permission.X)` is this module's equivalent of
`api/dependencies.py::require_roles(...)`, used the same way at the
route-decorator level: `dependencies=[Depends(require_permission(Permission.LEADS_READ))]`.
"""

from __future__ import annotations

import enum

from fastapi import Depends

from lead_harvester.api.dependencies import User, get_current_user
from lead_harvester.api.errors import AuthorizationError


class Permission(str, enum.Enum):
    LEADS_READ = "leads.read"
    LEADS_EXPORT = "leads.export"
    LEADS_CREATE = "leads.create"
    SECTORS_MANAGE = "sectors.manage"
    SELECTION_MANAGE = "selection.manage"
    COMPLIANCE_READ = "compliance.read"
    COMPLIANCE_MANAGE = "compliance.manage"
    DELETIONS_FULFIL = "deletions.fulfil"
    OUTBOX_MANAGE = "outbox.manage"
    OPERATIONS_READ = "operations.read"
    AUDIT_READ = "audit.read"


_ADMIN_PERMISSIONS = frozenset(Permission)

_REVIEWER_PERMISSIONS = frozenset(
    {
        Permission.LEADS_READ,
        Permission.LEADS_CREATE,
        Permission.SELECTION_MANAGE,
        Permission.COMPLIANCE_READ,
        Permission.OPERATIONS_READ,
    }
)

_VIEWER_PERMISSIONS = frozenset(
    {
        Permission.LEADS_READ,
        Permission.COMPLIANCE_READ,
        Permission.OPERATIONS_READ,
    }
)

# The explicit permission matrix: role -> the exact set of permissions it
# holds. A role not present here (there shouldn't be one -- User.role is
# only ever "admin"/"reviewer"/"viewer", see api/dependencies.py) holds no
# permissions at all, same as an empty set would.
ROLE_PERMISSIONS: dict[str, frozenset[Permission]] = {
    "admin": _ADMIN_PERMISSIONS,
    "reviewer": _REVIEWER_PERMISSIONS,
    "viewer": _VIEWER_PERMISSIONS,
}


def role_has_permission(role: str, permission: Permission) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, frozenset())


def require_permission(permission: Permission):
    """
    FastAPI dependency factory -- use at the route-decorator level:
    `dependencies=[Depends(require_permission(Permission.LEADS_READ))]`,
    same pattern `api/dependencies.py::require_roles` already established
    for the coarser 3-role checks on drafts.py/resolution_reviews.py.
    """

    async def permission_checker(current_user: User = Depends(get_current_user)) -> User:
        if not role_has_permission(current_user.role, permission):
            raise AuthorizationError()
        return current_user

    return permission_checker
