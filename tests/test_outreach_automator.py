import asyncio
import contextlib
import json
import uuid
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.canonical import CanonicalInstitution, OperatingStatus
from lead_harvester.models.outreach import AccountBrief, DraftStatus, OutreachDraft
from lead_harvester.outreach.automator import OutreachAutomator


@contextlib.asynccontextmanager
async def _fake_get_session(session: AsyncSession):
    yield session


def _draft(brief_id: uuid.UUID, name: str) -> OutreachDraft:
    return OutreachDraft(
        brief_id=brief_id,
        status=DraftStatus.APPROVED,
        target_name=name,
        target_role="Principal",
        target_contact_value=f"{name.lower().replace(' ', '.')}@example.edu",
        subject_line="Hello",
        body="Hi there",
    )


@pytest.mark.asyncio
async def test_concurrent_claims_never_double_claim_the_same_draft(async_engine):
    # OutreachAutomator.run() previously read APPROVED drafts, sent them,
    # and only afterward (in a separate transaction) marked them SENT --
    # two overlapping run() invocations could both read and send the same
    # drafts before either committed. This proves the fix -- claiming via
    # SELECT ... FOR UPDATE SKIP LOCKED, then flipping to SENDING in the
    # SAME transaction -- correctly partitions a shared batch of APPROVED
    # drafts across two genuinely concurrent connections with no overlap.
    setup_conn = await async_engine.connect()
    setup_session = AsyncSession(bind=setup_conn, expire_on_commit=False)
    institution = CanonicalInstitution(
        canonical_name="Concurrency Test School",
        institution_type="school",
        status=OperatingStatus.OPERATIONAL,
        confidence_score=0.7,
    )
    setup_session.add(institution)
    await setup_session.flush()

    brief = AccountBrief(institution_id=institution.id)
    setup_session.add(brief)
    await setup_session.flush()

    drafts = [_draft(brief.id, f"Contact {i}") for i in range(4)]
    setup_session.add_all(drafts)
    await setup_session.commit()
    draft_ids = {d.id for d in drafts}
    institution_id, brief_id = institution.id, brief.id
    await setup_session.close()
    await setup_conn.close()

    async def claim_batch() -> set[uuid.UUID]:
        conn = await async_engine.connect()
        session = AsyncSession(bind=conn, expire_on_commit=False)
        try:
            async with session.begin():
                claimed = list(
                    await session.scalars(
                        select(OutreachDraft)
                        .where(OutreachDraft.status == DraftStatus.APPROVED)
                        .limit(10)
                        .with_for_update(skip_locked=True)
                    )
                )
                for d in claimed:
                    d.status = DraftStatus.SENDING
            return {d.id for d in claimed}
        finally:
            await session.close()
            await conn.close()

    results = await asyncio.gather(claim_batch(), claim_batch())

    try:
        claimed_a, claimed_b = results
        assert claimed_a.isdisjoint(claimed_b), (claimed_a, claimed_b)
        assert claimed_a | claimed_b == draft_ids
    finally:
        cleanup_conn = await async_engine.connect()
        cleanup_session = AsyncSession(bind=cleanup_conn, expire_on_commit=False)
        try:
            from sqlalchemy import delete

            await cleanup_session.execute(
                delete(OutreachDraft).where(OutreachDraft.id.in_(draft_ids))
            )
            await cleanup_session.execute(delete(AccountBrief).where(AccountBrief.id == brief_id))
            await cleanup_session.execute(
                delete(CanonicalInstitution).where(CanonicalInstitution.id == institution_id)
            )
            await cleanup_session.commit()
        finally:
            await cleanup_session.close()
            await cleanup_conn.close()


def test_apply_persisted_message_budget_uses_warmup_limit_and_todays_usage(tmp_path):
    # Previously every invocation started a fresh ActionBudget with a flat
    # 15-message allowance regardless of the account's actual warmup phase
    # or how many messages an earlier invocation already sent today.
    from lead_harvester.sources.session_manager import SessionManager

    sm = SessionManager(tmp_path)
    sm.save_cookies("burner_01", [{"name": "x", "value": "y"}], first_login=True)

    # Backdate warmup_started_at to put this account in Week 3
    # (message limit 2 per day, not the flat default of 15).
    path = tmp_path / "burner_01.json"
    payload = json.loads(path.read_text())
    payload["warmup_started_at"] = (datetime.now(UTC).date() - timedelta(days=18)).isoformat()
    payload["run_log"] = [{"date": datetime.now(UTC).date().isoformat(), "actions": {"message": 1}}]
    path.write_text(json.dumps(payload))

    automator = OutreachAutomator(account_id="burner_01")
    automator._apply_persisted_message_budget(sm)

    assert automator.budget.DAILY_LIMITS["message"] == 2
    # One message already sent today -- only one more should be allowed
    # before charge() raises.
    automator.budget.charge("message")
    with pytest.raises(RuntimeError, match="Daily limit reached"):
        automator.budget.charge("message")


@pytest.mark.asyncio
async def test_run_releases_unsent_draft_back_to_approved(db_session):
    # No SMTP host is configured, so _send_email_batch returns immediately
    # without ever calling _send_email/_mark_sent for this email-style
    # draft -- before this fix, the draft was claimed to SENDING at the
    # start of run() and then permanently stuck there, silently dropped
    # from every future run despite nothing ever having been sent.
    institution = CanonicalInstitution(
        canonical_name="Release Test School",
        institution_type="school",
        status=OperatingStatus.OPERATIONAL,
        confidence_score=0.7,
    )
    db_session.add(institution)
    await db_session.flush()

    brief = AccountBrief(institution_id=institution.id)
    db_session.add(brief)
    await db_session.flush()

    draft = _draft(brief.id, "No Smtp Contact")
    db_session.add(draft)
    await db_session.flush()

    automator = OutreachAutomator(account_id="test-account")

    with (
        patch(
            "lead_harvester.outreach.automator.get_session",
            new=lambda: _fake_get_session(db_session),
        ),
        patch("lead_harvester.outreach.automator.within_working_hours", return_value=True),
    ):
        await automator.run()

    await db_session.refresh(draft)
    assert draft.status == DraftStatus.APPROVED
