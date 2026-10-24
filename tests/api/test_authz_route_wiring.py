"""
End-to-end confirmation that authz.py's PERMISSIONS entries (beyond the
original drafts/resolution_reviews three) are actually wired onto their
routes via require_permission -- not just declared in the registry.
test_authz.py already covers the registry in isolation; this covers the
wiring, so a route decorator missing its dependencies=[...] line would
fail here even though the registry itself looks correct.

A syntactically valid, non-existent UUID is used for every path
parameter -- require_permission runs as part of dependency resolution,
before the route body, so a viewer is rejected with 403 regardless of
whether the referenced row exists.
"""

import contextlib
import uuid
from unittest.mock import patch

import pytest

from lead_harvester.api.dependencies import wait_for_pending_denial_audits

_DUMMY_ID = str(uuid.uuid4())


@contextlib.asynccontextmanager
async def _fake_get_session(session):
    yield session


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("method", "path", "json"),
    [
        ("POST", "/api/v1/compliance/suppressions", {"contact_value": "a@b.com", "reason": "test"}),
        ("DELETE", f"/api/v1/compliance/suppressions/{_DUMMY_ID}", None),
        (
            "POST",
            "/api/v1/compliance/deletion-requests",
            {"subject_type": "institution", "subject_id": _DUMMY_ID},
        ),
        ("POST", f"/api/v1/compliance/deletion-requests/{_DUMMY_ID}/fulfill", None),
        ("POST", f"/api/v1/compliance/deletion-requests/{_DUMMY_ID}/reject", {"reason": "test"}),
        ("POST", "/api/v1/daily-selection", {}),
        ("POST", f"/api/v1/daily-selection/{_DUMMY_ID}/consume", None),
        ("POST", f"/api/v1/daily-selection/{_DUMMY_ID}/release", None),
        ("POST", "/api/v1/outbox/process", None),
        ("POST", f"/api/v1/outbox/{_DUMMY_ID}/requeue", None),
        (
            "POST",
            "/api/v1/sectors",
            {"code": "test", "display_name": "Test", "institution_types": ["a"]},
        ),
        ("PATCH", f"/api/v1/sectors/{_DUMMY_ID}", {"display_name": "Renamed"}),
        ("POST", "/api/v1/verification/sweep", {}),
        ("POST", f"/api/v1/verification/flags/{_DUMMY_ID}/resolve", {}),
        ("POST", f"/api/v1/verification/flags/{_DUMMY_ID}/dismiss", {}),
        ("POST", f"/api/v1/verification/contacts/{_DUMMY_ID}/unreachable", {}),
    ],
)
async def test_viewer_is_denied_on_every_newly_protected_mutating_route(
    client_viewer, db_session, method, path, json
):
    # require_permission's denial path audits fire-and-forget on its own
    # get_session() -- bound to DATABASE_URL, not the test's db_session --
    # redirect it so the audit write lands against the test fixture, and
    # drain the background task before the patch is removed (matching
    # tests/api/test_dependencies.py's pattern).
    with patch(
        "lead_harvester.api.dependencies.get_session", new=lambda: _fake_get_session(db_session)
    ):
        response = await client_viewer.request(method, path, json=json)
        await wait_for_pending_denial_audits()
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_viewer_is_denied_on_manual_lead_creation(client_viewer, db_session):
    with patch(
        "lead_harvester.api.dependencies.get_session", new=lambda: _fake_get_session(db_session)
    ):
        response = await client_viewer.post("/api/v1/leads/manual", json={})
        await wait_for_pending_denial_audits()
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_viewer_is_denied_on_leads_export(client_viewer, db_session):
    with patch(
        "lead_harvester.api.dependencies.get_session", new=lambda: _fake_get_session(db_session)
    ):
        response = await client_viewer.get("/api/v1/exports/leads")
        await wait_for_pending_denial_audits()
    assert response.status_code == 403
