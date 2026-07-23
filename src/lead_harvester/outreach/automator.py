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
import os
import smtplib
import ssl
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.database import get_session
from lead_harvester.models import (
    AccountBrief,
    OutreachDraft,
    OutreachOutcome,
    DraftStatus,
)
from lead_harvester.sources.session_manager import SessionManager
from lead_harvester.sources.human_emulator import ActionBudget, within_working_hours


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

    async def run(self) -> None:
        """Send all approved outreach drafts that haven't been sent yet."""
        from sqlalchemy import select

        if not within_working_hours():
            print("[Automator] Outside working hours. Will not send messages now.")
            return

        if self.dry_run:
            print("[Automator] DRY RUN MODE — messages will be typed but NOT sent.")

        async with get_session() as session:
            drafts = list(await session.scalars(
                select(OutreachDraft)
                .where(OutreachDraft.status == DraftStatus.APPROVED)
                .limit(10)
            ))

        if not drafts:
            print("[Automator] No approved drafts to send.")
            return

        print(f"[Automator] Found {len(drafts)} approved draft(s) to send.")

        # Open browser session once for all LinkedIn messages
        li_drafts = [d for d in drafts if d.target_contact_value.startswith("http")]
        email_drafts = [d for d in drafts if "@" in d.target_contact_value]

        if li_drafts:
            await self._send_linkedin_batch(li_drafts)

        if email_drafts:
            await self._send_email_batch(email_drafts)

    # ------------------------------------------------------------------
    # LinkedIn batch
    # ------------------------------------------------------------------

    async def _send_linkedin_batch(self, drafts: list[OutreachDraft]) -> None:
        try:
            from camoufox.async_api import AsyncCamoufox
        except ImportError:
            print("[Automator] camoufox not installed. Skipping LinkedIn sends.")
            return

        sm = SessionManager(self.sessions_dir)
        if not sm.has_session(self.account_id):
            print("[Automator] No LinkedIn session saved. Cannot send LinkedIn messages.")
            return

        cookies = sm.load_cookies(self.account_id)
        launch_kwargs: dict[str, Any] = {"humanize": True, "headless": False, "addons": []}
        if self.proxy:
            launch_kwargs["proxy"] = {"server": self.proxy}

        async with AsyncCamoufox(**launch_kwargs) as browser:
            context = await browser.new_context(
                locale="en-US",
                timezone_id="Asia/Karachi",
            )
            await context.add_cookies(cookies)
            page = await context.new_page()

            # Warm up feed first
            await page.goto("https://www.linkedin.com/feed/", wait_until="networkidle", timeout=30_000)
            await asyncio.sleep(15)

            for draft in drafts:
                await self._send_linkedin_message(page, draft)

            updated = await context.cookies()
            sm.save_cookies(self.account_id, updated)
            await context.close()

    async def _send_linkedin_message(self, page: Any, draft: OutreachDraft) -> None:
        from lead_harvester.sources.human_emulator import (
            action_pause, human_click, human_type, post_connect_pause, short_pause
        )
        from sqlalchemy import select

        profile_url = draft.target_contact_value

        try:
            self.budget.charge("message")
        except RuntimeError as e:
            print(f"[Automator] {e}")
            return

        try:
            await page.goto(profile_url, wait_until="networkidle", timeout=30_000)
            await action_pause()

            msg_btn = await page.query_selector("button[aria-label*='Message']")
            if not msg_btn:
                print(f"[Automator] ✗ No Message button for {profile_url} — skipping.")
                return

            await msg_btn.click()
            await action_pause()

            message_text = draft.body
            if self.dry_run:
                print(f"[Automator] DRY RUN — would type to {draft.target_name}:\n{message_text[:100]}...")
                await asyncio.sleep(3)
            else:
                await human_type(page, ".msg-form__contenteditable", message_text)
                await action_pause()
                send_btn = await page.query_selector("button.msg-form__send-button")
                if send_btn:
                    await send_btn.click()
                    print(f"[Automator] ✓ LinkedIn message sent to {draft.target_name}")
                    await self._mark_sent(draft)
                    await post_connect_pause()

        except Exception as e:
            print(f"[Automator] ✗ LinkedIn message failed for {draft.target_name}: {e}")

    # ------------------------------------------------------------------
    # Email batch
    # ------------------------------------------------------------------

    async def _send_email_batch(self, drafts: list[OutreachDraft]) -> None:
        if not self.smtp_host:
            print("[Automator] No SMTP configured. Skipping email sends.")
            return

        for draft in drafts:
            await self._send_email(draft)

    async def _send_email(self, draft: OutreachDraft) -> None:
        recipient = draft.target_contact_value

        if self.dry_run:
            print(f"[Automator] DRY RUN — would email {recipient}:\n"
                  f"Subject: {draft.subject_line}\n{draft.body[:100]}...")
            return

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = draft.subject_line
            msg["From"]    = f"{self.smtp_from_name} <{self.smtp_user}>"
            msg["To"]      = recipient

            # Plain text body
            msg.attach(MIMEText(draft.body, "plain"))

            ctx = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.ehlo()
                server.starttls(context=ctx)
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.smtp_user, recipient, msg.as_string())

            print(f"[Automator] ✓ Email sent to {recipient} ({draft.target_name})")
            await self._mark_sent(draft)

        except Exception as e:
            print(f"[Automator] ✗ Email failed to {recipient}: {e}")

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
                    recorded_at=datetime.now(timezone.utc),
                )
                session.add(outcome)
