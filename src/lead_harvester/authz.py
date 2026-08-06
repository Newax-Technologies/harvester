"""
Explicit permission catalog (docs/ROADMAP.md Module 05 /
docs/delivery/agency-intelligence-implementation-sequence.md Slice 1.3).

Replaces ad-hoc require_roles(*roles) string-literal checks scattered
across route decorators with named permissions, so a protected action
states *what* it protects (e.g. "drafts.decide") rather than only which
role names happen to satisfy it today. Deny-by-default: a permission
absent from PERMISSIONS, or a role not listed for a permission that IS
present, is denied -- see api/dependencies.py::require_permission, the
actual enforcement point.

Every route that mutates state, or that read-only routes depend on to
stay safe (governed exports), maps to a permission here -- this is
Gate 1's "every protected action maps to a permission" exit criterion
(docs/delivery/agency-intelligence-implementation-sequence.md). Pure
read (GET) endpoints stay authentication-only (any role, including
viewer, may call them) -- that is an intentional, minimal default, not
an oversight: nothing here restricts who can *see* data, only who can
change it or pull it in bulk. Every set below matches the three
pre-existing permissions' {reviewer, admin} shape, so viewer is
read-only everywhere and reviewer/admin can act -- the one place this
repo has drawn an admin-only line so far is credential issuance
(services/auth_service.py), not any of these routes.
"""

from __future__ import annotations

_REVIEWER_AND_ADMIN = frozenset({"reviewer", "admin"})

PERMISSIONS: dict[str, frozenset[str]] = {
    "drafts.edit": _REVIEWER_AND_ADMIN,
    "drafts.decide": _REVIEWER_AND_ADMIN,
    "resolution_reviews.decide": _REVIEWER_AND_ADMIN,
    "compliance.suppressions.manage": _REVIEWER_AND_ADMIN,
    "compliance.deletion_requests.create": _REVIEWER_AND_ADMIN,
    "compliance.deletion_requests.decide": _REVIEWER_AND_ADMIN,
    "compliance.deletion_requests.fulfill": _REVIEWER_AND_ADMIN,
    "daily_selection.trigger": _REVIEWER_AND_ADMIN,
    "daily_selection.manage": _REVIEWER_AND_ADMIN,
    "manual_leads.create": _REVIEWER_AND_ADMIN,
    "outbox.manage": _REVIEWER_AND_ADMIN,
    "sectors.manage": _REVIEWER_AND_ADMIN,
    "verification.manage": _REVIEWER_AND_ADMIN,
    "exports.leads": _REVIEWER_AND_ADMIN,
}


def is_permitted(permission: str, role: str) -> bool:
    return role in PERMISSIONS.get(permission, frozenset())
