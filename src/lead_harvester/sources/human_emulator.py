"""
Human Emulator — makes automated actions look genuinely human.

Covers:
- Gaussian-randomised delays (not uniform, not constant)
- Bézier-curve mouse movement (not straight lines)
- Character-by-character typing with per-key variance
- Natural scroll simulation
- "Coffee break" idle periods
- Working-hours guard
"""

from __future__ import annotations

import asyncio
import random
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from playwright.async_api import Page


# ---------------------------------------------------------------------------
# Time helpers
# ---------------------------------------------------------------------------


def _gauss_clamp(mu: float, sigma: float, lo: float, hi: float) -> float:
    """Gaussian sample clamped to [lo, hi]."""
    return max(lo, min(hi, random.gauss(mu, sigma)))


async def short_pause() -> None:
    """Brief micro-pause between small interactions (0.3 – 1.8 s)."""
    await asyncio.sleep(_gauss_clamp(0.8, 0.4, 0.3, 1.8))


async def action_pause() -> None:
    """Pause between distinct actions on a page (3 – 25 s)."""
    await asyncio.sleep(_gauss_clamp(10, 5, 3, 25))


async def between_profiles_pause() -> None:
    """Pause between visiting different profiles (45 – 240 s)."""
    await asyncio.sleep(_gauss_clamp(90, 40, 45, 240))


async def post_connect_pause() -> None:
    """Longer pause after sending a connection request (2 – 8 min)."""
    await asyncio.sleep(_gauss_clamp(300, 90, 120, 480))


async def feed_reading_pause() -> None:
    """Simulate reading the LinkedIn feed for 3 – 12 min."""
    await asyncio.sleep(_gauss_clamp(450, 120, 180, 720))


async def coffee_break() -> None:
    """Random 'coffee break' idle (5 – 35 min). Triggered occasionally."""
    await asyncio.sleep(_gauss_clamp(1200, 400, 300, 2100))


async def idle_drift(page: Page) -> None:
    """
    Simulate an unfocused user — move the mouse to a random spot and
    leave it still for a moment, like looking away from the screen.
    Only called occasionally between actions.
    """
    try:
        x = random.uniform(100, 900)
        y = random.uniform(100, 600)
        await page.mouse.move(x, y)
        await asyncio.sleep(_gauss_clamp(4.0, 1.5, 1.5, 10.0))
    except Exception as e:
        # Best-effort cosmetic mouse movement -- the page may have navigated
        # away mid-animation, which is not an error worth stopping for.
        print(f"human_emulator mouse jiggle skipped: {e}")


def session_start_delay_seconds(preferred_hour: int, jitter_minutes: int) -> float:
    """
    Calculate how many seconds to wait before starting a session so that
    it begins near the account's 'preferred' start time, not at a fixed clock time.
    This prevents LinkedIn from seeing the same session-start pattern daily.

    Returns 0 if we are already past today's start window.
    """
    now = datetime.now(UTC)
    # Convert PKT preferred_hour to UTC (PKT = UTC+5)
    target_utc_hour = (preferred_hour - 5) % 24
    jitter = random.randint(-jitter_minutes, jitter_minutes)
    # jitter_minutes can be as large as 45 (device_profile.py's generator
    # draws preferred_start_jitter from range(10, 45)), so 30 + jitter can
    # fall well outside 0-59 -- passing that directly as `minute=` to
    # datetime.replace() raises ValueError before the crawler ever opens a
    # browser. Building a valid base time first and adding the jitter as a
    # timedelta lets it carry across hour (and date) boundaries correctly
    # instead.
    base = now.replace(hour=target_utc_hour, minute=30, second=0, microsecond=0)
    target = base + timedelta(minutes=jitter)
    if target < now:
        return 0.0
    return (target - now).total_seconds()


def is_weekday() -> bool:
    """Return True if today is Monday–Friday (avoid weekends)."""
    return datetime.now(UTC).weekday() < 5


async def simulate_tab_blur(page: Page) -> None:
    """
    Fire browser blur/focus events to simulate the user Alt-Tabbing away
    and coming back (e.g. checking Slack, reading an email).
    LinkedIn's JS listens for these events. A session that never loses
    focus is a bot signal.
    """
    try:
        await page.evaluate("""
            document.dispatchEvent(new Event('visibilitychange'));
            window.dispatchEvent(new Event('blur'));
        """)
        # Simulate being away for 15–90 seconds
        await asyncio.sleep(_gauss_clamp(40, 20, 15, 90))
        await page.evaluate("""
            document.dispatchEvent(new Event('visibilitychange'));
            window.dispatchEvent(new Event('focus'));
        """)
    except Exception as e:
        # Best-effort blur/focus simulation -- the page may have navigated
        # away mid-sequence, which is not an error worth stopping for.
        print(f"human_emulator tab-blur simulation skipped: {e}")


async def dwell_for_content(page: Page) -> None:
    """
    Wait proportionally to the amount of text on the page, as if reading it.
    A 200-word page warrants ~50s dwell; a 800-word page warrants ~190s.
    Reading speed: ~250 words/min with Gaussian variance.
    """
    try:
        word_count: int = await page.evaluate(
            "() => document.body.innerText.split(/\\s+/).filter(Boolean).length"
        )
        reading_minutes = word_count / _gauss_clamp(250, 40, 150, 400)
        dwell_seconds = reading_minutes * 60
        # Clamp: minimum 8s (glance), maximum 4 minutes (deep read)
        dwell_seconds = max(8.0, min(240.0, dwell_seconds))
        await asyncio.sleep(_gauss_clamp(dwell_seconds, dwell_seconds * 0.15, 8, 240))
    except Exception:
        await action_pause()  # Fallback


async def human_scroll_with_reversal(
    page: Page,
    direction: str = "down",
    amount: int = 3,
) -> None:
    """
    Scroll with random backward reversals — as if re-reading a section.
    Humans don't scroll linearly; they go back up 15–25% of the time.
    """
    sign = 1 if direction == "down" else -1
    viewport = await page.evaluate("() => ({ h: window.innerHeight })")
    h = viewport.get("h", 800)

    total_px = h * amount
    scrolled = 0
    while scrolled < total_px:
        # Occasional reversal — scroll back up slightly
        if scrolled > 200 and random.random() < 0.20:
            reversal = random.randint(80, 250)
            await page.mouse.wheel(0, -reversal)
            scrolled = max(0, scrolled - reversal)
            await asyncio.sleep(_gauss_clamp(1.5, 0.5, 0.8, 3.5))

        chunk = random.randint(80, 300)
        await page.mouse.wheel(0, sign * chunk)
        scrolled += chunk
        await asyncio.sleep(_gauss_clamp(0.18, 0.07, 0.08, 0.5))

        # Occasional read-pause mid-scroll
        if random.random() < 0.12:
            await asyncio.sleep(_gauss_clamp(2.5, 1.0, 1.0, 6.0))


def within_working_hours(tz_offset_hours: int = 5) -> bool:
    """
    Return True if local time is between 09:00 and 18:30.
    Default offset +5 = Pakistan Standard Time.
    """
    now_utc = datetime.now(UTC)
    local_hour = (now_utc.hour + tz_offset_hours) % 24
    local_minute = now_utc.minute
    start = 9 * 60  # 09:00
    end = 18 * 60 + 30  # 18:30
    current = local_hour * 60 + local_minute
    return start <= current <= end


# ---------------------------------------------------------------------------
# Mouse movement — Bézier curves
# ---------------------------------------------------------------------------


def _bezier_point(t: float, pts: list[tuple[float, float]]) -> tuple[float, float]:
    """De Casteljau algorithm for an n-point Bézier curve."""
    pts = list(pts)
    while len(pts) > 1:
        pts = [
            (pts[i][0] * (1 - t) + pts[i + 1][0] * t, pts[i][1] * (1 - t) + pts[i + 1][1] * t)
            for i in range(len(pts) - 1)
        ]
    return pts[0]


async def human_move_to(page: Page, x: float, y: float) -> None:
    """
    Move the mouse to (x, y) along a randomised Bézier curve
    with 2 random control points to mimic human hand jitter.
    """
    current = await page.evaluate("() => ({ x: window.mouseX || 0, y: window.mouseY || 0 })")
    sx, sy = float(current.get("x", 0)), float(current.get("y", 0))

    # Two random control points introduce natural curve
    cx1 = sx + random.uniform(-200, 200)
    cy1 = sy + random.uniform(-150, 150)
    cx2 = x + random.uniform(-200, 200)
    cy2 = y + random.uniform(-150, 150)

    steps = random.randint(20, 40)
    for i in range(steps + 1):
        t = i / steps
        # Ease-in-out so the cursor doesn't start/stop abruptly
        t_eased = t * t * (3 - 2 * t)
        px, py = _bezier_point(t_eased, [(sx, sy), (cx1, cy1), (cx2, cy2), (x, y)])
        await page.mouse.move(px, py)
        await asyncio.sleep(_gauss_clamp(0.01, 0.005, 0.003, 0.03))


async def human_click(page: Page, selector: str) -> None:
    """Locate element, Bézier-move to it, then click with a small pre-click pause."""
    element = await page.wait_for_selector(selector, timeout=15_000)
    if element is None:
        raise RuntimeError(f"Element not found: {selector}")
    box = await element.bounding_box()
    if box is None:
        await element.click()
        return
    # Click slightly off-centre (humans don't aim perfectly)
    tx = box["x"] + box["width"] * random.uniform(0.3, 0.7)
    ty = box["y"] + box["height"] * random.uniform(0.3, 0.7)
    await human_move_to(page, tx, ty)
    await short_pause()
    await page.mouse.click(tx, ty)


# ---------------------------------------------------------------------------
# Typing — character-by-character with per-key variance
# ---------------------------------------------------------------------------


async def human_type(page: Page, selector: str, text: str) -> None:
    """
    Click into a field, then type text character-by-character with
    realistic per-keystroke delays, occasional typos with self-correction,
    and 'thinking pauses' at word boundaries.
    """
    await human_click(page, selector)
    await short_pause()
    i = 0
    while i < len(text):
        char = text[i]

        # Occasionally make a realistic typo and correct it (~3% chance per char)
        if char.isalpha() and random.random() < 0.03:
            # Type a wrong adjacent key, then backspace
            wrong = random.choice("qwertyuiopasdfghjklzxcvbnm")
            await page.keyboard.type(wrong, delay=0)
            await asyncio.sleep(_gauss_clamp(0.12, 0.05, 0.06, 0.30))
            await page.keyboard.press("Backspace")
            await asyncio.sleep(_gauss_clamp(0.20, 0.08, 0.10, 0.45))

        await page.keyboard.type(char, delay=0)

        # Base typing speed ~70 wpm; sigma adds jitter
        delay = _gauss_clamp(0.10, 0.05, 0.04, 0.35)

        # Thinking pause after word boundary
        if char == " " and random.random() < 0.08:
            delay += _gauss_clamp(0.6, 0.2, 0.3, 1.5)

        # Extra pause at punctuation (end of sentence feel)
        if char in ".,!?;:" and random.random() < 0.4:
            delay += _gauss_clamp(0.4, 0.15, 0.2, 0.9)

        await asyncio.sleep(delay)
        i += 1


# ---------------------------------------------------------------------------
# Scrolling
# ---------------------------------------------------------------------------


async def human_scroll(page: Page, direction: str = "down", amount: int = 3) -> None:
    """
    Scroll in increments with variable speed to mimic reading.
    direction: 'down' | 'up'
    amount: approximate number of 'screen heights' to scroll
    """
    sign = 1 if direction == "down" else -1
    viewport = await page.evaluate("() => ({ h: window.innerHeight })")
    h = viewport.get("h", 800)

    total_px = h * amount
    scrolled = 0
    while scrolled < total_px:
        chunk = random.randint(80, 300)
        await page.mouse.wheel(0, sign * chunk)
        scrolled += chunk
        await asyncio.sleep(_gauss_clamp(0.18, 0.07, 0.08, 0.5))
        # Occasional read-pause mid-scroll
        if random.random() < 0.12:
            await asyncio.sleep(_gauss_clamp(2.5, 1.0, 1.0, 6.0))


# ---------------------------------------------------------------------------
# Suspicious-action detector
# ---------------------------------------------------------------------------


class ActionBudget:
    """
    Enforces safe daily action limits.
    If a limit is exceeded, raises RuntimeError so the caller can
    gracefully stop for the day.
    """

    DAILY_LIMITS: ClassVar[dict[str, int]] = {
        "profile_view": 50,
        "search": 20,
        "connect": 10,
        "message": 15,
        "page_load": 200,
    }

    def __init__(self) -> None:
        self._counts: dict[str, int] = {k: 0 for k in self.DAILY_LIMITS}

    def charge(self, action: str, n: int = 1) -> None:
        limit = self.DAILY_LIMITS.get(action)
        if limit is None:
            return
        self._counts[action] = self._counts.get(action, 0) + n
        if self._counts[action] > limit:
            raise RuntimeError(
                f"Daily limit reached for '{action}' "
                f"({self._counts[action]}/{limit}). Stopping for today."
            )

    def remaining(self, action: str) -> int:
        limit = self.DAILY_LIMITS.get(action, 0)
        return max(0, limit - self._counts.get(action, 0))

    def summary(self) -> dict[str, str]:
        return {k: f"{self._counts.get(k, 0)}/{v}" for k, v in self.DAILY_LIMITS.items()}
