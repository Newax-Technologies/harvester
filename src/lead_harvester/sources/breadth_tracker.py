"""
Breadth Tracker
===============
Tracks which industries, companies, and geographic areas have been
visited across ALL accounts so the platform-level coverage breadth
stays low and non-systematic.

LinkedIn's 30-day detection window looks at COVERAGE BREADTH:
  "3 accounts visited every school principal in Karachi this month"
  is a detection signal even if each account only did 5 profiles/day.

The breadth tracker enforces:
  1. Zero URL overlap between accounts (strict partitioning)
  2. Industry mixing: for every N target visits, include noise visits
  3. Geographic pacing: don't finish one city before spreading to others
  4. 30-day breadth ceiling per vertical per geographic area

Storage: sessions/breadth_log.json (shared across all accounts)
"""

from __future__ import annotations

import json
import random
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

BREADTH_LOG_PATH = Path("sessions") / "breadth_log.json"

# Maximum profiles to visit per (vertical, city) combination in a 30-day window
# across ALL accounts combined. Keeps coverage non-systematic.
MAX_BREADTH_PER_VERTICAL_CITY_30D = 40


class BreadthTracker:
    """
    Shared breadth tracker used by all accounts in the farm.
    Persisted to disk so it survives between runs.
    """

    def __init__(self, log_path: Path = BREADTH_LOG_PATH) -> None:
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._data = self._load()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _load(self) -> dict[str, Any]:
        if self.log_path.exists():
            try:
                return json.loads(self.log_path.read_text())
            except Exception as e:
                print(f"breadth log at {self.log_path} is unreadable, starting fresh: {e}")
        return {"visits": [], "partitions": {}}

    def _save(self) -> None:
        self.log_path.write_text(json.dumps(self._data, indent=2))

    # ------------------------------------------------------------------
    # URL partitioning — zero overlap between accounts
    # ------------------------------------------------------------------

    def assign_partitions(
        self,
        urls: list[str],
        accounts: list[str],
        limits: dict[str, int],  # account_id -> profile_view limit today
        *,
        vertical: str = "unknown",
        target_city: str = "unknown",
        noise_urls: list[str] | None = None,
    ) -> dict[str, list[str]]:
        """
        Permanently assign URL segments to accounts so the same URL
        is NEVER visited by two different accounts.

        Existing assignments are preserved across runs.
        New URLs are assigned to the account with the lowest total allocation.

        vertical/target_city declare what this whole `urls` batch targets
        (e.g. "school principals in Karachi") -- the actual city a scraped
        profile reports isn't known until AFTER it's visited, so this is the
        only signal available at assignment time to enforce the 30-day
        breadth ceiling (is_breadth_exceeded) before any of these URLs are
        ever visited. Once a (vertical, city) combination has hit that
        ceiling across ALL accounts, no further URLs from ANY batch
        targeting the same combination are handed out -- not just new ones,
        but any still-unvisited backlog from a previous partition too,
        since executing it would push the same detectable combination
        further past the cap this tracker exists to hold.

        noise_urls (optional): a pool of off-target-vertical profile URLs.
        Any account whose needs_noise_visit() is due gets one (not yet
        visited by anyone, and not already handed to another account this
        call) spliced into its work list ahead of its real target URLs --
        the whole point of a noise visit is that it happens BEFORE the next
        target visit. The chosen URL is remembered (via _pending_noise) so
        the caller can record it with industry="noise" instead of the
        batch's real vertical once it's actually visited.
        """
        if self.is_breadth_exceeded(vertical, target_city):
            print(
                f"[BreadthTracker] 30-day breadth ceiling reached for "
                f"vertical={vertical!r} city={target_city!r} "
                f"({MAX_BREADTH_PER_VERTICAL_CITY_30D} visits across all accounts) -- "
                "assigning no further work for this combination."
            )
            return {a: [] for a in accounts}

        partitions: dict[str, list[str]] = self._data.setdefault("partitions", {})

        # Build reverse map: url -> assigned account
        url_to_account: dict[str, str] = {}
        for acc, acc_urls in partitions.items():
            for u in acc_urls:
                url_to_account[u] = acc

        # Assign unallocated URLs
        eligible = [a for a in accounts if limits.get(a, 0) > 0]
        if not eligible:
            return {a: [] for a in accounts}

        unassigned = [u for u in urls if u not in url_to_account]
        random.shuffle(unassigned)

        # Round-robin assignment weighted by remaining capacity
        for i, url in enumerate(unassigned):
            account = eligible[i % len(eligible)]
            partitions.setdefault(account, []).append(url)
            url_to_account[url] = account

        self._save()

        # Build today's work queue: assigned URLs not yet visited, capped by limit
        result: dict[str, list[str]] = {}
        visited_urls = {v["url"] for v in self._data.get("visits", [])}

        for acc in accounts:
            acc_urls = [u for u in partitions.get(acc, []) if u not in visited_urls]
            limit = limits.get(acc, 0)
            # Geographic pacing: shuffle so we don't visit the same city block
            random.shuffle(acc_urls)
            result[acc] = acc_urls[:limit]

        if noise_urls:
            self._inject_noise_visits(result, accounts, noise_urls, visited_urls)

        return result

    def _inject_noise_visits(
        self,
        result: dict[str, list[str]],
        accounts: list[str],
        noise_urls: list[str],
        visited_urls: set[str],
    ) -> None:
        pending_noise: dict[str, str] = self._data.setdefault("pending_noise", {})
        # A noise URL already flagged for some account (this call or an
        # earlier one whose visit hasn't landed yet) must not also be
        # handed to a different account -- that would violate the same
        # zero-overlap guarantee assign_partitions gives every other URL.
        claimed = set(pending_noise.keys()) | visited_urls
        changed = False
        for acc in accounts:
            if not self.needs_noise_visit(acc):
                continue
            candidate = next((u for u in noise_urls if u not in claimed), None)
            if candidate is None:
                continue
            claimed.add(candidate)
            pending_noise[candidate] = acc
            changed = True
            result[acc] = [candidate, *result.get(acc, [])]
        if changed:
            self._save()

    def consume_noise_marker(self, account_id: str, url: str) -> bool:
        """
        Returns True and forgets this URL once if it was injected as this
        account's noise visit (see _inject_noise_visits) -- lets the caller
        record it with industry="noise" instead of the batch's real
        vertical when logging the actual visit.
        """
        pending_noise: dict[str, str] = self._data.setdefault("pending_noise", {})
        if pending_noise.get(url) == account_id:
            del pending_noise[url]
            self._save()
            return True
        return False

    # ------------------------------------------------------------------
    # Visit logging and breadth checking
    # ------------------------------------------------------------------

    def record_visit(
        self,
        account_id: str,
        url: str,
        industry: str = "unknown",
        city: str = "unknown",
    ) -> None:
        """Log a profile visit with metadata for breadth analysis."""
        self._data.setdefault("visits", []).append(
            {
                "account_id": account_id,
                "url": url,
                "industry": industry.lower().strip(),
                "city": city.lower().strip(),
                "date": datetime.now(UTC).date().isoformat(),
            }
        )
        self._save()

    def is_breadth_exceeded(self, industry: str, city: str) -> bool:
        """
        Return True if this (industry, city) combination has already
        been visited MAX_BREADTH_PER_VERTICAL_CITY_30D times in the
        past 30 days across all accounts.
        """
        cutoff = (datetime.now(UTC).date() - timedelta(days=30)).isoformat()
        count = sum(
            1
            for v in self._data.get("visits", [])
            if v.get("industry", "").lower() == industry.lower()
            and v.get("city", "").lower() == city.lower()
            and v.get("date", "") >= cutoff
        )
        return count >= MAX_BREADTH_PER_VERTICAL_CITY_30D

    def already_visited(self, url: str) -> bool:
        """Return True if any account has ever visited this URL."""
        return any(v["url"] == url for v in self._data.get("visits", []))

    # ------------------------------------------------------------------
    # Noise injection
    # ------------------------------------------------------------------

    def needs_noise_visit(self, account_id: str) -> bool:
        """
        Return True if the account should do a 'noise' visit (a profile
        outside the target vertical) before its next real target visit.

        Rule: Every 4 target visits, inject 1 noise visit.
        """
        today = datetime.now(UTC).date().isoformat()
        today_visits = [
            v
            for v in self._data.get("visits", [])
            if v.get("account_id") == account_id and v.get("date") == today
        ]
        target_visits = [v for v in today_visits if v.get("industry") != "noise"]
        noise_visits = [v for v in today_visits if v.get("industry") == "noise"]

        if not target_visits:
            return False
        # Inject noise every 4th target visit
        return len(target_visits) % 4 == 0 and len(noise_visits) < len(target_visits) // 4

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def print_status(self) -> None:
        """Print a 30-day breadth summary per vertical/city."""
        cutoff = (datetime.now(UTC).date() - timedelta(days=30)).isoformat()
        visits = [v for v in self._data.get("visits", []) if v.get("date", "") >= cutoff]
        counter: dict[tuple[str, str], int] = defaultdict(int)
        for v in visits:
            counter[(v.get("industry", "?"), v.get("city", "?"))] += 1

        print(f"\n{'=' * 60}")
        print("  Breadth Tracker — Last 30 Days")
        print(f"{'=' * 60}")
        print(f"  {'Industry':<20} {'City':<15} {'Visits':>8} {'Ceiling':>8}")
        print(f"  {'-' * 55}")
        for (ind, city), count in sorted(counter.items(), key=lambda x: -x[1]):
            flag = " ⚠ NEAR LIMIT" if count >= MAX_BREADTH_PER_VERTICAL_CITY_30D * 0.7 else ""
            print(f"  {ind:<20} {city:<15} {count:>8} {MAX_BREADTH_PER_VERTICAL_CITY_30D:>8}{flag}")
        print(f"{'=' * 60}\n")
