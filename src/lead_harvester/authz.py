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

Only the three actions that previously used require_roles are registered
here. Every other route currently enforces authentication only (any
role, including viewer, may call it) -- that is the true current state,
not an oversight of this module, and broadening enforcement per-endpoint
is a separate product/security decision, not something this catalog
should silently decide by omission.
"""

from __future__ import annotations

PERMISSIONS: dict[str, frozenset[str]] = {
    "drafts.edit": frozenset({"reviewer", "admin"}),
    "drafts.decide": frozenset({"reviewer", "admin"}),
    "resolution_reviews.decide": frozenset({"reviewer", "admin"}),
}


def is_permitted(permission: str, role: str) -> bool:
    return role in PERMISSIONS.get(permission, frozenset())
