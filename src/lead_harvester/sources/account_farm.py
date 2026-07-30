"""
Account Farm Orchestrator
=========================
Distributes LinkedIn profile URLs across a pool of burner accounts,
each running as a completely isolated identity:

  ✓ Separate Camoufox browser process per account
  ✓ Separate session cookies (separate LinkedIn login)
  ✓ Separate device fingerprint (screen, CPU, memory, User-Agent)
  ✓ Separate geolocation (different Pakistani city per account)
  ✓ Separate timing patterns (different preferred start hours)
  ✓ Separate proxy (if configured)
  ✓ Separate warmup schedule tracked independently

Architecture:
  Each account runs in its own subprocess (not just an async task),
  so even the Python process, memory space, and OS-level fingerprints
  are fully isolated. LinkedIn cannot correlate them.

Usage (CLI):
  lead-harvester linkedin-farm-run \\
      --accounts burner_01,burner_02,burner_03 \\
      --urls-file targets.txt \\
      --proxies proxies.txt \\        # optional, one proxy per line
      --vertical school_principals \\ # optional, declares this batch's target vertical
      --target-city karachi \\        # optional, declares this batch's target city
      --noise-urls-file noise.txt     # optional, off-target profiles for noise injection

Usage (Python):
  farm = AccountFarm(accounts=["burner_01", "burner_02"])
  await farm.run(urls, vertical="school_principals", target_city="karachi")
"""

from __future__ import annotations

import asyncio
import multiprocessing
import queue as queue_module
import random
import threading
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from ..database import get_session
from ..models.source import RawSourceRecord, RunStatus, SourceRun, SourceType
from .breadth_tracker import BreadthTracker
from .device_profile import DeviceProfileManager
from .human_emulator import is_weekday, within_working_hours
from .session_manager import SessionManager

# ---------------------------------------------------------------------------
# Per-account job result
# ---------------------------------------------------------------------------


@dataclass
class AccountResult:
    account_id: str
    profiles_scraped: int = 0
    errors: list[str] = field(default_factory=list)
    city: str = ""
    warmup_phase: int = 0
    # The actual scraped profile data (as plain dicts, picklable across the
    # subprocess boundary via multiprocessing.Queue) -- without this, a
    # successful farm run reported profiles_scraped > 0 but never wrote a
    # single RawSourceRecord, silently discarding everything the workers
    # harvested and leaving linkedin-research nothing to process.
    profiles: list[dict] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Day-of-week scheduling — accounts operate on staggered days
# so they never all appear active simultaneously
# ---------------------------------------------------------------------------

# Map account index -> list of weekday numbers (0=Mon, 4=Fri) it should run on
# e.g. account 0 -> Mon+Tue, account 1 -> Wed+Thu, account 2 -> Fri
_WEEKDAY_SCHEDULES = [
    [0, 1],  # Mon, Tue
    [2, 3],  # Wed, Thu
    [4],  # Fri
    [0, 2, 4],  # Mon, Wed, Fri  (for 4th account onward, spread it)
    [1, 3],  # Tue, Thu
]


def account_scheduled_today(account_id: str, accounts: list[str]) -> bool:
    """
    Return True if this account is scheduled to operate today.
    Accounts are staggered across weekdays so they don't all
    appear simultaneously active (coordinated schedule = bot signal).
    """
    today_weekday = __import__("datetime").date.today().weekday()
    try:
        idx = accounts.index(account_id)
    except ValueError:
        return True  # Unknown account — let it run
    schedule = _WEEKDAY_SCHEDULES[idx % len(_WEEKDAY_SCHEDULES)]
    return today_weekday in schedule


# ---------------------------------------------------------------------------
# Worker — runs in a subprocess per account
# ---------------------------------------------------------------------------


def _run_account_worker(
    account_id: str,
    urls: list[str],
    proxy: str | None,
    captcha_key: str | None,
    result_queue: multiprocessing.Queue[dict],
) -> None:
    """
    Subprocess entry point. Each account worker is a completely isolated
    Python process with its own event loop and browser instance.
    """
    import asyncio as _asyncio
    import dataclasses

    async def _inner() -> dict:
        # Local imports inside subprocess — completely isolated import state
        from lead_harvester.sources.device_profile import DeviceProfileManager
        from lead_harvester.sources.linkedin_stealth import LinkedInStealthCrawler
        from lead_harvester.sources.session_manager import SessionManager

        sm = SessionManager("sessions")
        dpm = DeviceProfileManager("sessions")

        if not sm.has_session(account_id):
            return {
                "account_id": account_id,
                "profiles_scraped": 0,
                "errors": [f"No session saved for {account_id}. Run linkedin-login first."],
                "city": "",
                "warmup_phase": 0,
                "profiles": [],
            }

        device = dpm.get(account_id)
        limits = sm.get_today_limits(account_id)

        print(f"\n{'=' * 55}")
        print(f"  [{account_id}] City: {device.city_name}")
        print(f"  [{account_id}] Phase: {limits['phase_label']}")
        print(f"  [{account_id}] URLs to scrape: {len(urls)}")
        print(f"{'=' * 55}\n")

        crawler = LinkedInStealthCrawler(
            account_id=account_id,
            target_urls=urls,
            captcha_api_key=captcha_key,
            proxy=proxy,
        )
        try:
            profiles = await crawler.run()
            return {
                "account_id": account_id,
                "profiles_scraped": len(profiles),
                "errors": [],
                "city": device.city_name,
                "warmup_phase": limits.get("phase", 0),
                # Plain dicts (not the dataclass instances) so this crosses
                # the multiprocessing.Queue boundary without depending on
                # LinkedInProfile being importable/picklable identically on
                # the receiving end.
                "profiles": [dataclasses.asdict(p) for p in profiles],
            }
        except Exception as e:
            # A CAPTCHA-triggered abort, a search-budget exhaustion, or any
            # other browser-level failure escaping crawler.run() after
            # earlier URLs already succeeded previously discarded every
            # profile harvested so far by unconditionally returning an
            # empty list here. run() attaches whatever it collected before
            # the exception to partial_profiles -- persist that instead.
            partial_profiles = getattr(e, "partial_profiles", None) or []
            return {
                "account_id": account_id,
                "profiles_scraped": len(partial_profiles),
                "errors": [str(e)],
                "city": device.city_name,
                "warmup_phase": limits.get("phase", 0),
                "profiles": [dataclasses.asdict(p) for p in partial_profiles],
            }

    result = _asyncio.run(_inner())
    result_queue.put(result)


def _drain_result_queue(
    result_queue: multiprocessing.Queue,
    results: list[AccountResult],
    stop_event: threading.Event,
) -> None:
    """
    Continuously pulls finished-worker payloads off result_queue while
    account subprocesses are still running, instead of waiting until every
    p.join() has returned. A worker's result dict (profile lists can
    include experience/raw_html_snippet data) is large enough to fill the
    queue's underlying OS pipe buffer; multiprocessing.Queue.put() then
    blocks the worker until the pipe is read from. Draining only after all
    joins meant the parent could be stuck in p.join() waiting for a worker
    that itself was stuck in put() waiting for the parent to read -- a
    deadlock resolved only by the 7200s per-process timeout, which then
    terminates the worker and discards everything it harvested. Runs in a
    background thread so it can drain concurrently with the (blocking)
    process launches/joins in AccountFarm.run().
    """
    while True:
        try:
            data = result_queue.get(timeout=0.5)
        except queue_module.Empty:
            if stop_event.is_set():
                return
            continue
        results.append(AccountResult(**data))


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------


class AccountFarm:
    """
    Manages a pool of burner accounts, distributes work, and runs
    each account in its own isolated subprocess.

    Parameters
    ----------
    accounts : list[str]
        List of burner account IDs (e.g. ["burner_01", "burner_02"]).
    proxies : dict[str, str] | None
        Optional mapping of account_id → proxy string.
        e.g. {"burner_01": "http://user:pass@proxy1:8080"}
    captcha_key : str | None
        2Captcha API key (shared across all accounts).
    """

    def __init__(
        self,
        accounts: list[str],
        proxies: dict[str, str] | None = None,
        captcha_key: str | None = None,
    ) -> None:
        self.accounts = accounts
        self.proxies = proxies or {}
        self.captcha_key = captcha_key
        self.sm = SessionManager("sessions")
        self.dpm = DeviceProfileManager("sessions")

    def print_farm_status(self) -> None:
        """Print a summary table of all accounts in the farm."""
        print(f"\n{'=' * 70}")
        print(f"  ACCOUNT FARM STATUS  ({len(self.accounts)} accounts)")
        print(f"{'=' * 70}")
        print(f"  {'Account':<16} {'City':<14} {'Age':>5} {'Phase':<50}")
        print(f"  {'-' * 66}")

        for acc in self.accounts:
            if not self.sm.has_session(acc):
                print(f"  {acc:<16} {'NO SESSION':<14}  —    Run linkedin-login first")
                continue
            try:
                limits = self.sm.get_today_limits(acc)
                device = self.dpm.get(acc)
                age = limits.get("account_age_days", 0)
                phase = limits.get("phase_label", "")[:48]
                print(f"  {acc:<16} {device.city_name:<14} {age:>4}d  {phase}")
            except Exception as e:
                print(f"  {acc:<16} ERROR: {e}")

        print(f"{'=' * 70}\n")

    async def run(
        self,
        urls: list[str],
        *,
        vertical: str = "unknown",
        target_city: str = "unknown",
        noise_urls: list[str] | None = None,
    ) -> list[AccountResult]:
        """
        Distribute URLs across accounts and run each in its own subprocess.
        Uses BreadthTracker for zero-overlap URL partitioning and
        day-of-week scheduling to stagger accounts across the week.

        vertical/target_city declare what this `urls` batch targets (e.g.
        "school_principals" in "karachi") -- see BreadthTracker.
        assign_partitions for why this is the only signal available before
        any of these URLs are actually visited, and how it enforces the
        30-day breadth ceiling. noise_urls is an optional pool of off-target
        profiles used to satisfy BreadthTracker.needs_noise_visit for any
        account that's due one.
        """
        if not within_working_hours():
            print("[Farm] Outside working hours. Aborting.")
            return []

        if not is_weekday():
            print("[Farm] Weekend — no LinkedIn activity today. Aborting.")
            return []

        bt = BreadthTracker()

        # Build today's limits for every account
        today_limits: dict[str, dict] = {}
        per_account_limits: dict[str, int] = {}
        for acc in self.accounts:
            if self.sm.has_session(acc):
                limits = self.sm.get_today_limits(acc)
                today_limits[acc] = limits
                per_account_limits[acc] = limits.get("profile_view", 0)

        # Apply day-of-week scheduling — not all accounts run every day
        scheduled_today: list[str] = []
        skipped_today: list[str] = []
        for acc in self.accounts:
            if account_scheduled_today(acc, self.accounts):
                scheduled_today.append(acc)
            else:
                skipped_today.append(acc)
                print(f"[Farm] {acc} — not scheduled today (staggered schedule).")

        # Zero out limits for accounts not scheduled today
        for acc in skipped_today:
            per_account_limits[acc] = 0

        # Use BreadthTracker for zero-overlap URL partitioning, the 30-day
        # breadth ceiling, and noise injection
        assignment = bt.assign_partitions(
            urls,
            scheduled_today,
            per_account_limits,
            vertical=vertical,
            target_city=target_city,
            noise_urls=noise_urls,
        )

        # For Phase-1 or unscheduled accounts, assign empty list (feed warmup only)
        for acc in self.accounts:
            if acc not in assignment and self.sm.has_session(acc) and acc in scheduled_today:
                assignment[acc] = []

        self.print_farm_status()
        bt.print_status()

        # Launch each account as a separate subprocess
        result_queue: multiprocessing.Queue = multiprocessing.Queue()
        processes: list[multiprocessing.Process] = []

        for account_id, account_urls in assignment.items():
            proxy = self.proxies.get(account_id)
            p = multiprocessing.Process(
                target=_run_account_worker,
                args=(account_id, account_urls, proxy, self.captcha_key, result_queue),
                name=f"linkedin-{account_id}",
                daemon=True,
            )
            processes.append(p)

        # Drain the queue concurrently with launching/joining workers below
        # -- see _drain_result_queue's docstring for why draining only
        # after every p.join() had returned could deadlock and silently
        # discard harvested profiles on large payloads.
        results: list[AccountResult] = []
        stop_draining = threading.Event()
        drainer = threading.Thread(
            target=_drain_result_queue,
            args=(result_queue, results, stop_draining),
            daemon=True,
        )
        drainer.start()

        # Stagger launches 30–120s — all accounts opening at the same second
        # is a coordination signal (cross-account schedule correlation)
        for p in processes:
            p.start()
            stagger_secs = random.uniform(30, 120)
            print(f"[Farm] Started {p.name}. Waiting {stagger_secs:.0f}s before next...")
            await asyncio.sleep(stagger_secs)

        # Wait for all subprocesses to finish
        for p in processes:
            p.join(timeout=7200)
            if p.is_alive():
                print(f"[Farm] {p.name} timed out. Terminating.")
                p.terminate()
                p.join()

        # Every process has exited by now, so nothing further will ever be
        # put on the queue -- safe to stop the drainer once it empties.
        stop_draining.set()
        drainer.join()

        self._record_farm_visits(bt, results, vertical=vertical)
        await self._persist_profiles(results)

        # Print summary
        print(f"\n{'=' * 55}")
        print("  FARM RUN COMPLETE")
        print(f"{'=' * 55}")
        total = sum(r.profiles_scraped for r in results)
        for r in results:
            status = "✓" if not r.errors else "✗"
            print(
                f"  {status} {r.account_id:<16} [{r.city:<12}]  "
                f"{r.profiles_scraped} profiles scraped"
            )
            for err in r.errors:
                print(f"      Error: {err}")
        print(f"\n  Total profiles scraped today: {total}")
        print(f"{'=' * 55}\n")

        return results

    @staticmethod
    def _record_farm_visits(
        bt: BreadthTracker, results: list[AccountResult], *, vertical: str = "unknown"
    ) -> None:
        """
        Logs every profile a worker actually scraped into BreadthTracker's
        visit history. No caller anywhere recorded a visit before this --
        assign_partitions' own "not in visited_urls" exclusion, the 30-day
        MAX_BREADTH_PER_VERTICAL_CITY_30D ceiling (is_breadth_exceeded), and
        the every-4th-visit noise-injection scheduling (needs_noise_visit)
        all read the same self._data["visits"] list, so with nothing ever
        writing to it every one of those checks was permanently inert --
        the farm could keep re-visiting the exact same URLs indefinitely,
        which the breadth tracker exists specifically to prevent. Uses each
        profile's own reported location for the "city" dimension (the
        actual signal is_breadth_exceeded cares about -- which cities'
        profiles this URL set has been drawn from), falling back to
        "unknown" like record_visit's own default when a profile has none.

        `vertical` is the run's declared target vertical (see run()) --
        recorded as-is UNLESS this exact URL was injected as a noise visit
        for this account (assign_partitions' noise_urls path), in which
        case it's recorded as "noise" so needs_noise_visit's own target-vs-
        noise ratio check for future runs sees it correctly.
        """
        for result in results:
            for profile in result.profiles:
                url = profile.get("profile_url")
                if not url:
                    continue
                industry = "noise" if bt.consume_noise_marker(result.account_id, url) else vertical
                bt.record_visit(
                    result.account_id,
                    url,
                    industry=industry,
                    city=profile.get("location") or "unknown",
                )

    async def _persist_profiles(self, results: list[AccountResult]) -> None:
        """
        Writes every profile every worker scraped to RawSourceRecord, the
        same shape cli.py::linkedin_run already uses for the single-account
        path -- without this, a farm run reported profiles_scraped > 0 per
        account but the actual profile data (only ever returned to the
        parent process as a bare count) was discarded, leaving
        linkedin-research nothing to process despite the run "succeeding".
        """
        all_profiles = [(r.account_id, profile) for r in results for profile in r.profiles]
        if not all_profiles:
            return

        async with get_session() as session:
            run = SourceRun(
                source_type=SourceType.LINKEDIN,
                run_metadata={
                    "accounts": [r.account_id for r in results],
                    "profiles_found": len(all_profiles),
                },
                status=RunStatus.STARTED,
            )
            session.add(run)
            await session.flush()

            for account_id, profile in all_profiles:
                session.add(
                    RawSourceRecord(
                        source_run_id=run.id,
                        source_type=SourceType.LINKEDIN,
                        source_id=profile.get("profile_url", f"{account_id}:{uuid.uuid4().hex}"),
                        raw_payload=profile,
                        normalized_name=profile.get("full_name") or profile.get("company"),
                        normalized_phone=None,
                        normalized_domain=None,
                        location=None,
                    )
                )

            run.status = RunStatus.COMPLETED
            run.completed_at = datetime.now(UTC)

        print(f"[Farm] Saved {len(all_profiles)} profile(s) to the database.")
