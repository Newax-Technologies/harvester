import asyncio
import contextlib
import json
import uuid
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, patch

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


def test_reserve_message_budget_uses_warmup_limit_and_todays_usage(tmp_path):
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
    granted = automator._reserve_message_budget(sm, requested=10)

    # Week 3 limit is 2/day, 1 already sent today -- only 1 more available,
    # regardless of how many were requested.
    assert granted == 1
    assert automator.budget.DAILY_LIMITS["message"] == 1
    automator.budget.charge("message")
    with pytest.raises(RuntimeError, match="Daily limit reached"):
        automator.budget.charge("message")


def test_reserve_message_budget_is_logged_immediately_not_after_send(tmp_path):
    # The reservation itself must be visible to a second concurrent caller
    # before any message is actually sent -- otherwise two overlapping
    # runs could both read "0 used today" and each be granted the full
    # remaining allowance, since logging only after sending can't undo an
    # already-sent overage.
    from lead_harvester.sources.session_manager import SessionManager

    sm = SessionManager(tmp_path)
    sm.save_cookies("burner_02", [{"name": "x", "value": "y"}], first_login=True)
    path = tmp_path / "burner_02.json"
    payload = json.loads(path.read_text())
    payload["warmup_started_at"] = (datetime.now(UTC).date() - timedelta(days=18)).isoformat()
    path.write_text(json.dumps(payload))

    first_run = OutreachAutomator(account_id="burner_02")
    second_run = OutreachAutomator(account_id="burner_02")

    first_granted = first_run._reserve_message_budget(sm, requested=2)
    second_granted = second_run._reserve_message_budget(sm, requested=2)

    # Week 3 limit is 2/day total, split across the two overlapping runs --
    # neither call may see the other's grant as still-available headroom.
    assert first_granted + second_granted == 2


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


@pytest.mark.asyncio
async def test_run_does_not_requeue_draft_after_email_send_succeeds_but_mark_sent_fails(
    db_session,
):
    # sendmail() succeeding but the subsequent _mark_sent() DB write then
    # hitting a transient error previously left the draft counted as "not
    # sent" -- _release_unsent_drafts would revert it from SENDING back to
    # APPROVED, and the next run would email the same recipient a second
    # time even though the first email already went out.
    institution = CanonicalInstitution(
        canonical_name="Mark Sent Failure School",
        institution_type="school",
        status=OperatingStatus.OPERATIONAL,
        confidence_score=0.7,
    )
    db_session.add(institution)
    await db_session.flush()

    brief = AccountBrief(institution_id=institution.id)
    db_session.add(brief)
    await db_session.flush()

    draft = _draft(brief.id, "Mark Sent Failure Contact")
    db_session.add(draft)
    await db_session.flush()

    automator = OutreachAutomator(
        account_id="test-account",
        smtp_host="smtp.example.com",
        smtp_user="sender@example.com",
        smtp_password="secret",
    )
    automator._mark_sent = AsyncMock(side_effect=RuntimeError("transient db error"))

    with (
        patch(
            "lead_harvester.outreach.automator.get_session",
            new=lambda: _fake_get_session(db_session),
        ),
        patch("lead_harvester.outreach.automator.within_working_hours", return_value=True),
        patch("smtplib.SMTP") as mock_smtp,
    ):
        server = mock_smtp.return_value.__enter__.return_value
        await automator.run()

    server.sendmail.assert_called_once()
    automator._mark_sent.assert_awaited_once()

    # The email genuinely went out -- must stay claimed (SENDING), not be
    # silently reverted to APPROVED where a future run would send it again.
    # (The real get_session() commits the claim-to-SENDING transition when
    # its `async with` block exits; _fake_get_session doesn't, and neither
    # the mocked _mark_sent nor the short-circuited _release_unsent_drafts
    # touch the session again here, so an explicit flush stands in for that
    # commit before reloading from the database.)
    await db_session.flush()
    await db_session.refresh(draft)
    assert draft.status == DraftStatus.SENDING


@pytest.mark.asyncio
async def test_run_skips_linkedin_batch_when_restricted_sources_disabled(db_session):
    # docs/ROADMAP.md Module 28: LinkedIn account automation stays
    # Restricted until explicit approval. Settings.restricted_sources_enabled
    # defaults to False, so a LinkedIn draft must never even be claimed by
    # the batch query -- it stays untouched (APPROVED) rather than being
    # claimed, found policy-blocked, and released back.
    institution = CanonicalInstitution(
        canonical_name="Restricted Source School",
        institution_type="school",
        status=OperatingStatus.OPERATIONAL,
        confidence_score=0.7,
    )
    db_session.add(institution)
    await db_session.flush()

    brief = AccountBrief(institution_id=institution.id)
    db_session.add(brief)
    await db_session.flush()

    li_draft = OutreachDraft(
        brief_id=brief.id,
        status=DraftStatus.APPROVED,
        target_name="LinkedIn Contact",
        target_role="Principal",
        target_contact_value="https://www.linkedin.com/in/someone",
        subject_line="Hello",
        body="Hi there",
    )
    db_session.add(li_draft)
    await db_session.flush()

    automator = OutreachAutomator(account_id="test-account")
    automator._send_linkedin_batch = AsyncMock(side_effect=AssertionError("must not be called"))

    with (
        patch(
            "lead_harvester.outreach.automator.get_session",
            new=lambda: _fake_get_session(db_session),
        ),
        patch("lead_harvester.outreach.automator.within_working_hours", return_value=True),
    ):
        result = await automator.run()

    # A run whose ONLY approved work was policy-blocked LinkedIn drafts
    # must report failure -- a scheduler must be able to tell that apart
    # from a genuinely empty/successful run.
    assert result is False
    automator._send_linkedin_batch.assert_not_awaited()
    await db_session.refresh(li_draft)
    assert li_draft.status == DraftStatus.APPROVED


@pytest.mark.asyncio
async def test_run_still_sends_email_batch_when_linkedin_batch_is_restricted(db_session):
    # A mixed batch must not let a policy-disabled LinkedIn channel block an
    # unrelated, fully-allowed email send in the same run() call.
    institution = CanonicalInstitution(
        canonical_name="Mixed Batch School",
        institution_type="school",
        status=OperatingStatus.OPERATIONAL,
        confidence_score=0.7,
    )
    db_session.add(institution)
    await db_session.flush()

    brief = AccountBrief(institution_id=institution.id)
    db_session.add(brief)
    await db_session.flush()

    li_draft = OutreachDraft(
        brief_id=brief.id,
        status=DraftStatus.APPROVED,
        target_name="LinkedIn Contact",
        target_role="Principal",
        target_contact_value="https://www.linkedin.com/in/someone-else",
        subject_line="Hello",
        body="Hi there",
    )
    email_draft = _draft(brief.id, "Email Contact")
    db_session.add_all([li_draft, email_draft])
    await db_session.flush()

    automator = OutreachAutomator(
        account_id="test-account",
        smtp_host="smtp.example.com",
        smtp_user="sender@example.com",
        smtp_password="secret",
    )
    automator._send_linkedin_batch = AsyncMock(side_effect=AssertionError("must not be called"))

    with (
        patch(
            "lead_harvester.outreach.automator.get_session",
            new=lambda: _fake_get_session(db_session),
        ),
        patch("lead_harvester.outreach.automator.within_working_hours", return_value=True),
        patch("smtplib.SMTP") as mock_smtp,
    ):
        server = mock_smtp.return_value.__enter__.return_value
        result = await automator.run()

    # A mixed batch whose email drafts sent is a success, even though the
    # LinkedIn portion was policy-blocked (and, per the query filter,
    # never claimed at all).
    assert result is True
    server.sendmail.assert_called_once()
    automator._send_linkedin_batch.assert_not_awaited()
    await db_session.refresh(li_draft)
    await db_session.refresh(email_draft)
    assert li_draft.status == DraftStatus.APPROVED
    assert email_draft.status == DraftStatus.SENT


@pytest.mark.asyncio
async def test_run_never_sends_to_a_suppressed_contact(db_session):
    # Nothing checked suppression before docs/ROADMAP.md module 11 --
    # OutreachAutomator sent to any APPROVED draft unconditionally, so an
    # opted-out or bounced contact could be messaged again on the very
    # next run. A suppressed draft must be excluded from the send batch
    # and released back to APPROVED (the same path used for any other
    # unattempted draft), not sent.
    from lead_harvester.models.compliance import SuppressionEntry, SuppressionReason

    institution = CanonicalInstitution(
        canonical_name="Suppressed Contact School",
        institution_type="school",
        status=OperatingStatus.OPERATIONAL,
        confidence_score=70.0,
    )
    db_session.add(institution)
    await db_session.flush()

    brief = AccountBrief(institution_id=institution.id)
    db_session.add(brief)
    await db_session.flush()

    draft = _draft(brief.id, "Suppressed Contact")
    db_session.add(draft)
    db_session.add(
        SuppressionEntry(
            normalized_contact_value=draft.target_contact_value,
            reason=SuppressionReason.OPT_OUT,
            note="unsubscribed",
        )
    )
    await db_session.flush()

    automator = OutreachAutomator(
        account_id="test-account",
        smtp_host="smtp.example.com",
        smtp_user="sender@example.com",
        smtp_password="secret",
    )

    with (
        patch(
            "lead_harvester.outreach.automator.get_session",
            new=lambda: _fake_get_session(db_session),
        ),
        patch("lead_harvester.outreach.automator.within_working_hours", return_value=True),
        patch("smtplib.SMTP") as mock_smtp,
    ):
        await automator.run()

    mock_smtp.assert_not_called()
    await db_session.refresh(draft)
    assert draft.status == DraftStatus.APPROVED


@pytest.mark.asyncio
async def test_run_reports_failure_when_smtp_send_fails_for_every_claimed_draft(db_session):
    # A claimed batch that genuinely failed to send (SMTP error) must not
    # be reported as a successful run just because something was
    # claimable -- a scheduler needs to be able to alert/retry on this,
    # the same way it already can for a policy-blocked LinkedIn batch.
    institution = CanonicalInstitution(
        canonical_name="Smtp Failure School",
        institution_type="school",
        status=OperatingStatus.OPERATIONAL,
        confidence_score=0.7,
    )
    db_session.add(institution)
    await db_session.flush()

    brief = AccountBrief(institution_id=institution.id)
    db_session.add(brief)
    await db_session.flush()

    draft = _draft(brief.id, "Smtp Failure Contact")
    db_session.add(draft)
    await db_session.flush()

    automator = OutreachAutomator(
        account_id="test-account",
        smtp_host="smtp.example.com",
        smtp_user="sender@example.com",
        smtp_password="secret",
    )

    with (
        patch(
            "lead_harvester.outreach.automator.get_session",
            new=lambda: _fake_get_session(db_session),
        ),
        patch("lead_harvester.outreach.automator.within_working_hours", return_value=True),
        patch("smtplib.SMTP", side_effect=OSError("connection refused")),
    ):
        result = await automator.run()

    assert result is False
    await db_session.refresh(draft)
    assert draft.status == DraftStatus.APPROVED


@pytest.mark.asyncio
async def test_run_reports_success_in_dry_run_mode_even_though_nothing_is_confirmed_sent(
    db_session,
):
    # Dry-run mode never actually sends anything by design (_send_email
    # always returns False when dry_run is set) -- that must not be
    # conflated with the SMTP-failure case above.
    institution = CanonicalInstitution(
        canonical_name="Dry Run School",
        institution_type="school",
        status=OperatingStatus.OPERATIONAL,
        confidence_score=0.7,
    )
    db_session.add(institution)
    await db_session.flush()

    brief = AccountBrief(institution_id=institution.id)
    db_session.add(brief)
    await db_session.flush()

    draft = _draft(brief.id, "Dry Run Contact")
    db_session.add(draft)
    await db_session.flush()

    automator = OutreachAutomator(
        account_id="test-account",
        smtp_host="smtp.example.com",
        smtp_user="sender@example.com",
        smtp_password="secret",
        dry_run=True,
    )

    with (
        patch(
            "lead_harvester.outreach.automator.get_session",
            new=lambda: _fake_get_session(db_session),
        ),
        patch("lead_harvester.outreach.automator.within_working_hours", return_value=True),
        patch("smtplib.SMTP") as mock_smtp,
    ):
        result = await automator.run()

    assert result is True
    mock_smtp.assert_not_called()
