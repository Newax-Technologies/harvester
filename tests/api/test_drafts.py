import pytest
from sqlalchemy import select

from lead_harvester.api.app import app
from lead_harvester.api.dependencies import User, get_current_user
from lead_harvester.models.audit import AuditLog


@pytest.mark.asyncio
async def test_second_reviewer_receives_409(client_a, client_b, seeded_draft, db_session):
    draft_a = await client_a.get(f"/api/v1/drafts/{seeded_draft.id}")
    draft_b = await client_b.get(f"/api/v1/drafts/{seeded_draft.id}")

    version = draft_a.json()["version"]
    assert draft_b.json()["version"] == version

    # Reviewer A approves
    app.dependency_overrides[get_current_user] = lambda: User(
        id="reviewer_A", username="Alice", role="reviewer"
    )
    approved = await client_a.post(
        f"/api/v1/drafts/{seeded_draft.id}/decision",
        json={
            "decision": "approved",
            "expected_version": version,
            "feedback": "Evidence checked.",
        },
    )
    assert approved.status_code == 200

    # Reviewer B attempts rejection using the stale version
    app.dependency_overrides[get_current_user] = lambda: User(
        id="reviewer_B", username="Bob", role="reviewer"
    )
    rejected = await client_b.post(
        f"/api/v1/drafts/{seeded_draft.id}/decision",
        json={
            "decision": "rejected",
            "expected_version": version,
            "feedback": "Outdated reviewer action.",
        },
    )

    assert rejected.status_code == 409
    assert rejected.json()["error"]["code"] == "stale_resource"

    # Assert state remains unchanged from Reviewer A
    await db_session.refresh(seeded_draft)
    assert seeded_draft.status.value == "approved"
    assert seeded_draft.version == version + 1

    # Assert Audit Logs
    result = await db_session.execute(
        select(AuditLog).where(AuditLog.entity_id == str(seeded_draft.id))
    )
    audits = result.scalars().all()
    assert len(audits) == 1
    assert audits[0].actor == "reviewer_A"

    assert audits[0].action == "draft.approved"
