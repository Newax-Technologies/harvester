"""
Session Manager — persists LinkedIn cookies per burner account so we never
have to automate the login flow (which reliably triggers 2FA / identity checks).

Also manages the account WARMUP SCHEDULE:
  LinkedIn's AI tracks velocity changes. A brand-new account that suddenly
  starts visiting 20 profiles/day will be flagged immediately.
  The warmup schedule ramps up activity gradually over 4 weeks, just like
  a real human getting more comfortable with the platform.

Warmup schedule (profile views per day):
  Day 1–3   : 0  — feed browsing only, NO profile visits
  Day 4–7   : 1  — 1 profile per day (Monday–Friday only)
  Week 2    : 3  — 3 profiles/day
  Week 3    : 8  — 8 profiles/day
  Week 4+   : 20 — full speed (our permanent safe limit)

Usage:
    manager = SessionManager("sessions")

    # First login
    manager.save_cookies("burner_01", cookies)

    # Every subsequent run — get today's allowed limits
    limits = manager.get_today_limits("burner_01")
    print(limits)  # {"profile_view": 3, "connect": 1, "message": 2, ...}
    cookies = manager.load_cookies("burner_01")
"""

from __future__ import annotations

import contextlib
import json
import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

if sys.platform != "win32":
    import fcntl
else:
    fcntl = None  # type: ignore[assignment]

SESSIONS_DIR = Path("sessions")

# A CAPTCHA means LinkedIn has flagged the session -- even a successful
# solve leaves it "watched", so every challenge enforces a mandatory rest
# before the account is used again, regardless of solve outcome.
CAPTCHA_COOLDOWN = timedelta(hours=24)


# ---------------------------------------------------------------------------
# Warmup schedule — (profile_views, connects, messages, searches) per day
# ---------------------------------------------------------------------------


def _warmup_limits(account_age_days: int) -> dict[str, int]:
    """
    Return safe daily action limits based on how old the account session is.
    """
    if account_age_days <= 3:
        # Feed-only phase — absolutely no profile visits
        return {
            "profile_view": 0,
            "connect": 0,
            "message": 0,
            "search": 0,
            "feed_scroll": 5,  # Just scroll the feed to look active
            "phase": 1,
            "phase_label": "Feed Warmup (Days 1–3): Browse feed only. No profile visits.",
        }
    elif account_age_days <= 7:
        # Gentle introduction
        return {
            "profile_view": 1,
            "connect": 0,  # No connects yet — too aggressive for a new account
            "message": 0,
            "search": 2,
            "feed_scroll": 5,
            "phase": 2,
            "phase_label": "Gentle Start (Days 4–7): 1 profile view/day. No connections yet.",
        }
    elif account_age_days <= 14:
        # Week 2
        return {
            "profile_view": 3,
            "connect": 1,
            "message": 0,
            "search": 5,
            "feed_scroll": 5,
            "phase": 3,
            "phase_label": "Week 2: 3 profile views/day. 1 connection request/day.",
        }
    elif account_age_days <= 21:
        # Week 3
        return {
            "profile_view": 8,
            "connect": 3,
            "message": 2,
            "search": 10,
            "feed_scroll": 5,
            "phase": 4,
            "phase_label": "Week 3: 8 profile views/day. 3 connections. 2 messages.",
        }
    else:
        # Week 4+ — full operating speed
        return {
            "profile_view": 20,
            "connect": 10,
            "message": 15,
            "search": 20,
            "feed_scroll": 5,
            "phase": 5,
            "phase_label": "Full Speed (Week 4+): 20 profiles/day. 10 connections. 15 messages.",
        }


class SessionManager:
    def __init__(self, base_dir: str | Path = SESSIONS_DIR) -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, account_id: str) -> Path:
        return self.base_dir / f"{account_id}.json"

    # ------------------------------------------------------------------
    # Cookie persistence
    # ------------------------------------------------------------------

    def save_cookies(
        self,
        account_id: str,
        cookies: list[dict[str, Any]],
        first_login: bool = False,
    ) -> None:
        """
        Persist cookies to disk after a manual login.
        If first_login=True, stamps the warmup start date.
        """
        path = self._path(account_id)

        # Preserve existing metadata (warmup_started_at, run_log) if present
        existing: dict[str, Any] = {}
        if path.exists():
            try:
                existing = json.loads(path.read_text())
            except Exception as e:
                print(f"session file for {account_id} is unreadable, overwriting: {e}")

        payload = {
            "account_id": account_id,
            "saved_at": datetime.now(UTC).isoformat(),
            "warmup_started_at": existing.get(
                "warmup_started_at", datetime.now(UTC).date().isoformat() if first_login else None
            ),
            "run_log": existing.get("run_log", []),
            # Without this, save_cookies (called from the crawler's own
            # cleanup finally-block after a CAPTCHA-triggered abort)
            # overwrote the whole session file and silently dropped the
            # last_captcha_at that record_captcha_challenge had JUST
            # written moments earlier in that same run -- the very next
            # invocation then saw no cooldown recorded at all and reused
            # the flagged account immediately.
            "last_captcha_at": existing.get("last_captcha_at"),
            "cookies": cookies,
        }

        path.write_text(json.dumps(payload, indent=2))
        print(f"[SessionManager] Saved {len(cookies)} cookies for '{account_id}'.")

    def load_cookies(self, account_id: str) -> list[dict[str, Any]]:
        """Load cookies. Raises FileNotFoundError if session not saved."""
        path = self._path(account_id)
        if not path.exists():
            raise FileNotFoundError(
                f"No saved session for '{account_id}'. "
                f"Run: lead-harvester linkedin-login --account {account_id}"
            )
        payload = json.loads(path.read_text())
        print(
            f"[SessionManager] Loaded {len(payload['cookies'])} cookies "
            f"for '{account_id}' (saved {payload['saved_at']})."
        )
        return payload["cookies"]

    # ------------------------------------------------------------------
    # Warmup schedule
    # ------------------------------------------------------------------

    @staticmethod
    def _account_age_days(payload: dict[str, Any]) -> int:
        warmup_str = payload.get("warmup_started_at")
        if not warmup_str:
            # Session exists but warmup date was never set — treat as day 0
            return 0
        warmup_start = date.fromisoformat(warmup_str)
        return (datetime.now(UTC).date() - warmup_start).days

    @staticmethod
    def _sum_actions_for_today(payload: dict[str, Any]) -> dict[str, int]:
        today = datetime.now(UTC).date().isoformat()
        totals: dict[str, int] = {}
        for entry in payload.get("run_log", []):
            if entry.get("date") != today:
                continue
            for action, count in entry.get("actions", {}).items():
                totals[action] = totals.get(action, 0) + count
        return totals

    def get_today_limits(self, account_id: str) -> dict[str, Any]:
        """
        Return today's allowed action limits for this account based on
        how many days it has been since first login.
        """
        path = self._path(account_id)
        if not path.exists():
            raise FileNotFoundError(f"No session for '{account_id}'.")

        payload = json.loads(path.read_text())
        account_age_days = self._account_age_days(payload)

        limits = _warmup_limits(account_age_days)
        limits["account_age_days"] = account_age_days
        return limits

    def actions_taken_today(self, account_id: str) -> dict[str, int]:
        """
        Sums every run_log entry recorded for today into per-action totals.
        run_log is append-only (one entry per past log_run call, never
        merged) -- callers that only check today's warmup-phase limit
        without also consulting this can be re-invoked any number of times
        in the same day and each get a fresh in-memory budget, letting the
        account's real daily action count blow past its configured limit.
        """
        path = self._path(account_id)
        if not path.exists():
            return {}
        payload = json.loads(path.read_text())
        return self._sum_actions_for_today(payload)

    def log_run(self, account_id: str, actions: dict[str, int]) -> None:
        """
        Record what actions were taken today into the session log.
        Useful for auditing how many actions have been taken over time.
        """
        path = self._path(account_id)
        if not path.exists():
            return
        payload = json.loads(path.read_text())
        payload.setdefault("run_log", []).append(
            {
                "date": datetime.now(UTC).date().isoformat(),
                "actions": actions,
            }
        )
        path.write_text(json.dumps(payload, indent=2))

    # ------------------------------------------------------------------
    # CAPTCHA cooldown
    # ------------------------------------------------------------------

    def record_captcha_challenge(self, account_id: str) -> None:
        """
        Persists the exact moment a CAPTCHA challenge appeared for this
        account. log_run's own date-only granularity is enough for daily
        warmup budgets, but a 24-hour rest has to be measured from the
        real moment of the challenge, not calendar-day boundaries.
        """
        path = self._path(account_id)
        if not path.exists():
            return
        payload = json.loads(path.read_text())
        payload["last_captcha_at"] = datetime.now(UTC).isoformat()
        path.write_text(json.dumps(payload, indent=2))

    def captcha_cooldown_remaining(self, account_id: str) -> timedelta:
        """
        Returns how much of the mandatory post-CAPTCHA rest is still left
        (timedelta(0) if none is outstanding). Previously nothing ever read
        the "captcha_triggered" event _check_for_captcha logged -- neither
        LinkedInStealthCrawler.run() nor the farm scheduler checked it
        before starting the account again, so the crawler's own claimed
        "mandatory 24-hour rest" was never actually enforced and a flagged
        account could be rerun immediately.
        """
        path = self._path(account_id)
        if not path.exists():
            return timedelta(0)
        payload = json.loads(path.read_text())
        last_str = payload.get("last_captcha_at")
        if not last_str:
            return timedelta(0)
        elapsed = datetime.now(UTC) - datetime.fromisoformat(last_str)
        return max(timedelta(0), CAPTCHA_COOLDOWN - elapsed)

    # ------------------------------------------------------------------
    # Atomic per-account budget reservation
    # ------------------------------------------------------------------

    @contextlib.contextmanager
    def _locked_session_file(self, account_id: str):
        """
        Holds an exclusive OS-level advisory lock on the account's session
        file for the duration of the block. Uses fcntl.flock on Unix;
        falls back to no-op locking on Windows (single-process usage).
        """
        path = self._path(account_id)
        if not path.exists():
            raise FileNotFoundError(f"No session for '{account_id}'.")
        with open(path, "r+", encoding="utf-8") as f:
            if fcntl is not None:
                fcntl.flock(f, fcntl.LOCK_EX)
            try:
                yield f
            finally:
                if fcntl is not None:
                    fcntl.flock(f, fcntl.LOCK_UN)

    def reserve_action(self, account_id: str, action: str, requested: int) -> int:
        """
        Atomically reserve up to `requested` units of `action` against
        today's warmup limit, logging the reservation before releasing the
        file lock. Returns how many units were actually granted (<=
        requested, >= 0).

        Without this, two overlapping runs for the same account (e.g. two
        `linkedin-send` invocations, or a crashed run retried while a
        second copy is still in flight) could both call
        actions_taken_today() before either one appended its own send
        count, each see the same "nothing used yet today" snapshot, and
        each receive the full remaining allowance -- collectively blowing
        past the account's real daily limit with no way to undo it after
        the fact. Logging the reservation as part of the same locked
        read-modify-write means the second run's own reservation call
        immediately sees the first run's reservation. Pair with
        release_action once the real send outcome is known, to give back
        any granted-but-unused portion (e.g. fewer drafts than granted, a
        missing Message button, or a per-message failure).
        """
        if requested <= 0:
            return 0
        with self._locked_session_file(account_id) as f:
            payload = json.loads(f.read())
            limit = _warmup_limits(self._account_age_days(payload)).get(action, 0)
            already_used = self._sum_actions_for_today(payload).get(action, 0)
            granted = max(0, min(requested, limit - already_used))
            if granted > 0:
                payload.setdefault("run_log", []).append(
                    {"date": datetime.now(UTC).date().isoformat(), "actions": {action: granted}}
                )
                f.seek(0)
                f.write(json.dumps(payload, indent=2))
                f.truncate()
            return granted

    def release_action(self, account_id: str, action: str, unused: int) -> None:
        """Give back the unused portion of a prior reserve_action grant."""
        if unused <= 0:
            return
        with self._locked_session_file(account_id) as f:
            payload = json.loads(f.read())
            payload.setdefault("run_log", []).append(
                {"date": datetime.now(UTC).date().isoformat(), "actions": {action: -unused}}
            )
            f.seek(0)
            f.write(json.dumps(payload, indent=2))
            f.truncate()

    def print_status(self, account_id: str) -> None:
        """Print a human-readable warmup status report."""
        limits = self.get_today_limits(account_id)
        age = limits["account_age_days"]

        path = self._path(account_id)
        payload = json.loads(path.read_text())
        runs = payload.get("run_log", [])
        today_runs = [r for r in runs if r.get("date") == datetime.now(UTC).date().isoformat()]

        print(f"\n{'=' * 60}")
        print(f"  Account:    {account_id}")
        print(f"  Age:        {age} day(s) since first login")
        print(f"  Phase:      {limits['phase_label']}")
        print("\n  Today's limits:")
        for k, v in limits.items():
            if k not in ("phase", "phase_label", "account_age_days"):
                print(f"    {k:<16}: {v}")
        if today_runs:
            print(f"\n  Actions taken today: {today_runs[-1].get('actions', {})}")
        print(f"{'=' * 60}\n")

    # ------------------------------------------------------------------
    # Misc helpers
    # ------------------------------------------------------------------

    def has_session(self, account_id: str) -> bool:
        return self._path(account_id).exists()

    def list_accounts(self) -> list[str]:
        return [p.stem for p in self.base_dir.glob("*.json")]

    def invalidate(self, account_id: str) -> None:
        """Delete a session (e.g. after a ban or cookie expiry)."""
        path = self._path(account_id)
        if path.exists():
            path.unlink()
            print(f"[SessionManager] Invalidated session for '{account_id}'.")
