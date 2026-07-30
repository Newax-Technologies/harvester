import pytest
from sqlalchemy import select

from lead_harvester.api.app import app
from lead_harvester.api.dependencies import User, get_current_user
from lead_harvester.models.audit import AuditLog
from lead_harvester.models.outreach import DraftStatus


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


@pytest.mark.asyncio
async def test_edit_rejected_while_draft_is_being_sent(client_a, seeded_draft, db_session):
    # OutreachAutomator.run() claims a draft to SENDING (without bumping
    # version) and loads its body into memory before that claim's own
    # commit. A reviewer's concurrent edit using the version they loaded
    # before the claim would otherwise still pass the version check and
    # silently mutate a body the automator is actively sending, leaving
    # the database recording content different from what was delivered.
    version = seeded_draft.version
    seeded_draft.status = DraftStatus.SENDING
    await db_session.commit()

    app.dependency_overrides[get_current_user] = lambda: User(
        id="reviewer_A", username="Alice", role="reviewer"
    )
    response = await client_a.patch(
        f"/api/v1/drafts/{seeded_draft.id}",
        json={"message": "Edited while sending!", "expected_version": version},
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "draft_being_sent"

    await db_session.refresh(seeded_draft)
    assert seeded_draft.body == "World"
    assert seeded_draft.status == DraftStatus.SENDING


@pytest.mark.asyncio
async def test_decision_rejected_while_draft_is_being_sent(client_a, seeded_draft, db_session):
    version = seeded_draft.version
    seeded_draft.status = DraftStatus.SENDING
    await db_session.commit()

    app.dependency_overrides[get_current_user] = lambda: User(
        id="reviewer_A", username="Alice", role="reviewer"
    )
    response = await client_a.post(
        f"/api/v1/drafts/{seeded_draft.id}/decision",
        json={
            "decision": "approved",
            "expected_version": version,
            "feedback": "Approving while it's already sending.",
        },
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "draft_being_sent"

    await db_session.refresh(seeded_draft)
    assert seeded_draft.status == DraftStatus.SENDING


@pytest.mark.asyncio
async def test_edit_rejected_after_draft_already_sent(client_a, seeded_draft, db_session):
    # The SENDING -> SENT transition doesn't bump version either (see
    # _mark_sent), so a stale-version edit loaded before the send would
    # otherwise still pass the version check and rewrite the recorded body
    # of a message that has already been delivered.
    version = seeded_draft.version
    seeded_draft.status = DraftStatus.SENT
    await db_session.commit()

    app.dependency_overrides[get_current_user] = lambda: User(
        id="reviewer_A", username="Alice", role="reviewer"
    )
    response = await client_a.patch(
        f"/api/v1/drafts/{seeded_draft.id}",
        json={"message": "Edited after sent!", "expected_version": version},
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "draft_being_sent"

    await db_session.refresh(seeded_draft)
    assert seeded_draft.body == "World"
    assert seeded_draft.status == DraftStatus.SENT


@pytest.mark.asyncio
async def test_decision_rejected_after_draft_already_sent(client_a, seeded_draft, db_session):
    # Without this, a stale-version decision could move an already-SENT
    # draft back to APPROVED, letting the next automator run send it again.
    version = seeded_draft.version
    seeded_draft.status = DraftStatus.SENT
    await db_session.commit()

    app.dependency_overrides[get_current_user] = lambda: User(
        id="reviewer_A", username="Alice", role="reviewer"
    )
    response = await client_a.post(
        f"/api/v1/drafts/{seeded_draft.id}/decision",
        json={
            "decision": "approved",
            "expected_version": version,
            "feedback": "Approving after it's already sent.",
        },
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "draft_being_sent"

    await db_session.refresh(seeded_draft)
    assert seeded_draft.status == DraftStatus.SENT
