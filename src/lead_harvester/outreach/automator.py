"""
Outreach Automator
==================
Takes approved OutreachDraft records from the database and sends them
via LinkedIn message (using the Camoufox session) and/or email (SMTP).

Workflow:
  1. Query OutreachDraft records with status=APPROVED from the database.
  2. For each draft:
     a. Send LinkedIn message via the stealth crawler.
        OR
     b. Send email via SMTP.
  3. Mark draft status as SENT and record OutreachOutcome.

All LinkedIn actions respect the same human-behaviour and budget rules
as the crawler.
"""

from __future__ import annotations

import asyncio
import smtplib
import ssl
import uuid
from datetime import UTC, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

from lead_harvester.compliance.source_policy import (
    RestrictedSourceDisabledError,
    ensure_source_enabled,
)
from lead_harvester.config import settings
from lead_harvester.database import get_session
from lead_harvester.models import (
    DraftStatus,
    OutreachDraft,
    OutreachOutcome,
)
from lead_harvester.models.source import SourceType
from lead_harvester.services.compliance_service import is_eligible_to_contact
from lead_harvester.sources.human_emulator import ActionBudget, within_working_hours
from lead_harvester.sources.session_manager import SessionManager


class OutreachAutomator:
    """
    Sends approved outreach drafts via LinkedIn and/or email.

    Parameters
    ----------
    account_id : str
        Burner LinkedIn account used by the stealth crawler.
    smtp_host / smtp_port / smtp_user / smtp_password : str
        SMTP credentials for email sending. Leave blank to skip email.
    captcha_api_key : str | None
        2Captcha key forwarded to the crawler.
    proxy : str | None
        Residential proxy string.
    dry_run : bool
        If True, types messages but does NOT click Send. Use for testing.
    """

    def __init__(
        self,
        account_id: str,
        smtp_host: str = "",
        smtp_port: int = 587,
        smtp_user: str = "",
        smtp_password: str = "",
        smtp_from_name: str = "NEWAX Sales",
        captcha_api_key: str | None = None,
        proxy: str | None = None,
        dry_run: bool = False,
        sessions_dir: str = "sessions",
    ) -> None:
        self.account_id = account_id
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.smtp_from_name = smtp_from_name
        self.captcha_api_key = captcha_api_key
        self.proxy = proxy
        self.dry_run = dry_run
        self.budget = ActionBudget()
        self.sessions_dir = sessions_dir

    # ------------------------------------------------------------------
    # Main run loop
    # ------------------------------------------------------------------

    async def run(self) -> bool:
        """
        Send all approved outreach drafts that haven't been sent yet.
        Returns False only when nothing was claimable this run because
        every approved draft was a LinkedIn draft policy-blocked by
        restricted_sources_enabled=False -- a scheduler must be able to
        tell that apart from a genuinely successful (or truly empty) run.
        A mixed batch whose email drafts still sent, or a run with no
        approved drafts of any kind, both return True.
        """
        from sqlalchemy import select

        if not within_working_hours():
            print("[Automator] Outside working hours. Will not send messages now.")
            return True

        if self.dry_run:
            print("[Automator] DRY RUN MODE — messages will be typed but NOT sent.")

        # Excludes LinkedIn-shaped rows (target_contact_value is a URL) from
        # the claim itself when restricted sources are disabled -- claiming
        # them here only to immediately release them back to APPROVED still
        # ate a slot in the .limit(10) batch, capable of starving approved
        # email drafts behind a full page of policy-blocked LinkedIn rows on
        # every single run.
        restricted_sources_enabled = settings.restricted_sources_enabled
        claim_query = select(OutreachDraft).where(OutreachDraft.status == DraftStatus.APPROVED)
        if not restricted_sources_enabled:
            claim_query = claim_query.where(~OutreachDraft.target_contact_value.startswith("http"))

        # Atomically claim a batch: lock candidate rows (skipping any another
        # concurrent run() already has locked) and flip them to SENDING in
        # the SAME transaction before it commits, so two overlapping
        # invocations (or overlapping cron triggers) can never both read and
        # send the same APPROVED drafts. Known v1 limitation: a crash after
        # this commits but before the send completes leaves the draft
        # permanently stuck in SENDING with no automatic requeue -- a
        # stale-SENDING sweep is separate follow-up work, not solved here.
        async with get_session() as session:
            drafts = list(
                await session.scalars(claim_query.limit(10).with_for_update(skip_locked=True))
            )
            for draft in drafts:
                draft.status = DraftStatus.SENDING

        if not drafts:
            if not restricted_sources_enabled:
                blocked_backlog = await self._count_blocked_linkedin_backlog()
                if blocked_backlog:
                    print(
                        f"[Automator] {blocked_backlog} approved LinkedIn draft(s) waiting -- "
                        "blocked by policy (RESTRICTED_SOURCES_ENABLED=false), not sent."
                    )
                    return False
            print("[Automator] No approved drafts to send.")
            return True

        print(f"[Automator] Found {len(drafts)} approved draft(s) to send.")
        claimed_ids = [d.id for d in drafts]

        # Compliance gate (docs/ROADMAP.md module 11): never send to a
        # suppressed contact, regardless of how "approved" the draft is.
        # Nothing checked this before -- an opted-out or bounced contact
        # could be messaged again on the very next run. A suppressed draft
        # is simply excluded from li_drafts/email_drafts below, so it's
        # never attempted; _release_unsent_drafts' existing finally block
        # then reverts it to APPROVED like any other unattempted draft
        # (it isn't in confirmed_sent_ids). Known v1 limitation: this
        # means a suppressed draft stays APPROVED forever and gets
        # re-checked (and re-released) every run rather than moving to a
        # dedicated terminal status -- adding one is separate follow-up
        # work, not solved here, to avoid widening OutreachDraft's already
        # carefully-claimed state machine for this fix.
        suppressed_ids: set[uuid.UUID] = set()
        async with get_session() as session:
            for draft in drafts:
                channel = "linkedin" if draft.target_contact_value.startswith("http") else "email"
                result = await is_eligible_to_contact(session, draft.target_contact_value, channel)
                if not result.eligible:
                    suppressed_ids.add(draft.id)
                    print(f"[Automator] Skipping draft {draft.id} -- {result.reason}")
        if suppressed_ids:
            drafts = [d for d in drafts if d.id not in suppressed_ids]

        # Only a successful send calls _mark_sent (SENDING -> SENT) --
        # dry-run mode, a missing SMTP host, a missing camoufox install, no
        # saved LinkedIn session, an exhausted action budget, no Message
        # button on the profile, or any other per-draft send failure all
        # leave a claimed draft sitting in SENDING with nothing to ever move
        # it forward again, permanently removing it from every future run
        # even though nothing was actually sent. Release whatever this run
        # claimed but never sent back to APPROVED once every send attempt
        # has finished (or raised) -- a genuine process crash before this
        # point is the already-documented v1 limitation above, not solved
        # here, since it requires reaching this point at all.
        # Populated with the id of every draft whose external send action
        # (LinkedIn Send click, or SMTP sendmail) actually completed --
        # regardless of whether the subsequent _mark_sent() DB write itself
        # succeeded. A transient DB error in _mark_sent() must never be
        # treated the same as "the send failed": _release_unsent_drafts
        # below reverts every claimed-but-still-SENDING draft back to
        # APPROVED so the next run retries it, and retrying one that was
        # already delivered is a real, externally-visible double-send.
        confirmed_sent_ids: set[uuid.UUID] = set()
        try:
            # Open browser session once for all LinkedIn messages
            li_drafts = [d for d in drafts if d.target_contact_value.startswith("http")]
            email_drafts = [d for d in drafts if "@" in d.target_contact_value]

            if li_drafts:
                try:
                    ensure_source_enabled(
                        SourceType.LINKEDIN,
                        restricted_sources_enabled=settings.restricted_sources_enabled,
                    )
                except RestrictedSourceDisabledError as e:
                    # Leave li_drafts claimed-but-unsent -- the finally
                    # block's _release_unsent_drafts reverts them to
                    # APPROVED below, same as any other unsent draft in
                    # this batch, so a later enabled run retries them.
                    print(f"[Automator] LinkedIn batch skipped: {e}")
                else:
                    confirmed_sent_ids |= await self._send_linkedin_batch(li_drafts)

            if email_drafts:
                confirmed_sent_ids |= await self._send_email_batch(email_drafts)
        finally:
            await self._release_unsent_drafts(claimed_ids, confirmed_sent_ids)

        return True

    async def _count_blocked_linkedin_backlog(self) -> int:
        from sqlalchemy import func, select

        async with get_session() as session:
            return (
                await session.scalar(
                    select(func.count())
                    .select_from(OutreachDraft)
                    .where(
                        OutreachDraft.status == DraftStatus.APPROVED,
                        OutreachDraft.target_contact_value.startswith("http"),
                    )
                )
            ) or 0

    # ------------------------------------------------------------------
    # LinkedIn batch
    # ------------------------------------------------------------------

    def _reserve_message_budget(self, sm: SessionManager, requested: int) -> int:
        """
        Reserve this run's message allowance atomically (SessionManager.
        reserve_action), rather than separately reading today's usage and
        setting a local budget -- reading and later logging as two
        unlocked steps let two overlapping runs for the same account both
        see the same "nothing used yet" snapshot and each get the full
        remaining allowance, since logging only after sending cannot undo
        an already-sent overage. The granted amount becomes this run's
        entire DAILY_LIMITS["message"], starting from zero, since
        reserve_action already accounted for everything used earlier
        today. Same pattern as sources/linkedin_stealth.py's
        LinkedInStealthCrawler for the reservation call itself; unused
        units must be given back via sm.release_action once the real send
        outcome is known (see the `finally` block in _send_linkedin_batch).
        """
        granted = sm.reserve_action(self.account_id, "message", requested)
        self.budget.DAILY_LIMITS = {**self.budget.DAILY_LIMITS, "message": granted}
        self.budget._counts["message"] = 0
        return granted

    async def _send_linkedin_batch(self, drafts: list[OutreachDraft]) -> set[uuid.UUID]:
        confirmed_sent_ids: set[uuid.UUID] = set()
        try:
            from camoufox.async_api import AsyncCamoufox
        except ImportError:
            print("[Automator] camoufox not installed. Skipping LinkedIn sends.")
            return confirmed_sent_ids

        sm = SessionManager(self.sessions_dir)
        if not sm.has_session(self.account_id):
            print("[Automator] No LinkedIn session saved. Cannot send LinkedIn messages.")
            return confirmed_sent_ids

        reserved = self._reserve_message_budget(sm, len(drafts))
        messages_sent_this_run = 0

        cookies = sm.load_cookies(self.account_id)
        launch_kwargs: dict[str, Any] = {"humanize": True, "headless": False, "addons": []}
        if self.proxy:
            launch_kwargs["proxy"] = {"server": self.proxy}

        try:
            async with AsyncCamoufox(**launch_kwargs) as browser:
                context = await browser.new_context(
                    locale="en-US",
                    timezone_id="Asia/Karachi",
                )
                await context.add_cookies(cookies)
                page = await context.new_page()

                # Warm up feed first
                await page.goto(
                    "https://www.linkedin.com/feed/", wait_until="networkidle", timeout=30_000
                )
                await asyncio.sleep(15)

                for draft in drafts:
                    sent = await self._send_linkedin_message(page, draft)
                    if sent:
                        messages_sent_this_run += 1
                        confirmed_sent_ids.add(draft.id)

                updated = await context.cookies()
                sm.save_cookies(self.account_id, updated)
                await context.close()
        finally:
            # reserve_action already logged the full `reserved` amount up
            # front (see _reserve_message_budget) so a concurrent run sees
            # it immediately -- give back whatever portion of that
            # reservation this run didn't actually use (fewer drafts sent
            # than granted, a missing Message button, a per-message
            # failure, or an exception aborting the loop early). A draft
            # whose Send click succeeded counts as used here even if its
            # _mark_sent() DB write later failed (see _send_linkedin_message)
            # -- the click already happened, so this budget unit is spent
            # regardless of whether the database learned about it.
            unused = reserved - messages_sent_this_run
            if unused > 0:
                sm.release_action(self.account_id, "message", unused)

        return confirmed_sent_ids

    async def _send_linkedin_message(self, page: Any, draft: OutreachDraft) -> bool:
        """Returns True only if a real (non-dry-run) message was actually sent."""

        from lead_harvester.sources.human_emulator import (
            action_pause,
            human_type,
            post_connect_pause,
        )

        profile_url = draft.target_contact_value

        try:
            self.budget.charge("message")
        except RuntimeError as e:
            print(f"[Automator] {e}")
            return False

        try:
            await page.goto(profile_url, wait_until="networkidle", timeout=30_000)
            await action_pause()

            msg_btn = await page.query_selector("button[aria-label*='Message']")
            if not msg_btn:
                print(f"[Automator] ✗ No Message button for {profile_url} — skipping.")
                return False

            await msg_btn.click()
            await action_pause()

            message_text = draft.body
            if self.dry_run:
                print(
                    f"[Automator] DRY RUN — would type to {draft.target_name}:\n{message_text[:100]}..."
                )
                await asyncio.sleep(3)
                return False

            await human_type(page, ".msg-form__contenteditable", message_text)
            await action_pause()
            send_btn = await page.query_selector("button.msg-form__send-button")
            if not send_btn:
                return False

            await send_btn.click()
        except Exception as e:
            print(f"[Automator] ✗ LinkedIn message failed for {draft.target_name}: {e}")
            return False

        # The click above is a real, irreversible external action -- from
        # here on, a failure must not be reported as "the send failed".
        # _mark_sent()'s own DB write is isolated in its own try/except so a
        # transient failure there can't turn this into a False return: that
        # would both release this budget unit back into today's allowance
        # (see _send_linkedin_batch) and, since the draft is still SENDING
        # in the database, let _release_unsent_drafts revert it to APPROVED
        # -- causing a genuine second LinkedIn send next run for a message
        # that already went out. Leaving it stuck in SENDING instead is the
        # same accepted "needs manual review" outcome already documented for
        # a mid-send crash in run()'s docstring.
        print(f"[Automator] ✓ LinkedIn message sent to {draft.target_name}")
        try:
            await self._mark_sent(draft)
        except Exception as e:
            print(
                f"[Automator] ✗ Sent to {draft.target_name} but failed to record SENT "
                f"status: {e} -- leaving draft claimed (SENDING) rather than risk a "
                "double-send; needs manual review."
            )
        await post_connect_pause()
        return True

    # ------------------------------------------------------------------
    # Email batch
    # ------------------------------------------------------------------

    async def _send_email_batch(self, drafts: list[OutreachDraft]) -> set[uuid.UUID]:
        if not self.smtp_host:
            print("[Automator] No SMTP configured. Skipping email sends.")
            return set()

        confirmed_sent_ids: set[uuid.UUID] = set()
        for draft in drafts:
            if await self._send_email(draft):
                confirmed_sent_ids.add(draft.id)
        return confirmed_sent_ids

    async def _send_email(self, draft: OutreachDraft) -> bool:
        """Returns True only if sendmail() actually completed (dry-run never does)."""
        recipient = draft.target_contact_value

        if self.dry_run:
            print(
                f"[Automator] DRY RUN — would email {recipient}:\n"
                f"Subject: {draft.subject_line}\n{draft.body[:100]}..."
            )
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = draft.subject_line
            msg["From"] = f"{self.smtp_from_name} <{self.smtp_user}>"
            msg["To"] = recipient

            # Plain text body
            msg.attach(MIMEText(draft.body, "plain"))

            ctx = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.ehlo()
                server.starttls(context=ctx)
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.smtp_user, recipient, msg.as_string())
        except Exception as e:
            print(f"[Automator] ✗ Email failed to {recipient}: {e}")
            return False

        # sendmail() above is a real, irreversible external action -- from
        # here on, a failure must not be reported as "the send failed" (see
        # the matching comment in _send_linkedin_message). Isolating
        # _mark_sent() means a transient DB error recording SENT status
        # can't cause _release_unsent_drafts to revert this draft to
        # APPROVED and have it emailed a second time next run.
        print(f"[Automator] ✓ Email sent to {recipient} ({draft.target_name})")
        try:
            await self._mark_sent(draft)
        except Exception as e:
            print(
                f"[Automator] ✗ Sent to {recipient} but failed to record SENT status: "
                f"{e} -- leaving draft claimed (SENDING) rather than risk a "
                "double-send; needs manual review."
            )
        return True

    # ------------------------------------------------------------------
    # Database update
    # ------------------------------------------------------------------

    async def _mark_sent(self, draft: OutreachDraft) -> None:
        async with get_session() as session:
            db_draft = await session.get(OutreachDraft, draft.id)
            if db_draft:
                db_draft.status = DraftStatus.SENT
                outcome = OutreachOutcome(
                    draft_id=draft.id,
                    opened=False,
                    clicked=False,
                    replied=False,
                    recorded_at=datetime.now(UTC),
                )
                session.add(outcome)

    async def _release_unsent_drafts(
        self, claimed_ids: list[uuid.UUID], confirmed_sent_ids: set[uuid.UUID] | None = None
    ) -> None:
        from sqlalchemy import update

        # A draft in confirmed_sent_ids had its external send action (the
        # LinkedIn click, or sendmail()) actually complete, even if
        # _mark_sent()'s own DB write then failed and left it still SENDING
        # in the database -- see _send_linkedin_message/_send_email. Reverting
        # it to APPROVED here would have the next run send it again, a real
        # double-send for a message that already went out; leaving it stuck
        # in SENDING for manual review is the safer outcome.
        release_ids = [cid for cid in claimed_ids if cid not in (confirmed_sent_ids or set())]
        if not release_ids:
            return
        async with get_session() as session:
            await session.execute(
                update(OutreachDraft)
                .where(
                    OutreachDraft.id.in_(release_ids),
                    OutreachDraft.status == DraftStatus.SENDING,
                )
                .values(status=DraftStatus.APPROVED)
            )
