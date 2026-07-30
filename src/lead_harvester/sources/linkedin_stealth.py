"""
LinkedIn Stealth Crawler
========================
Uses Camoufox (Firefox-based anti-detect browser) to scrape LinkedIn
profiles at a human pace without triggering detection.

Anti-detection layers:
  ✓ Camoufox — patches at C++ engine level (WebGL, Canvas, Audio, TLS)
  ✓ Persistent cookie sessions (no automated login / 2FA)
  ✓ Gaussian-randomised delays between every action
  ✓ Bézier-curve mouse movement
  ✓ Character-by-character typing with variance
  ✓ Human scroll simulation
  ✓ Working-hours-only operation (09:00 – 18:30 PKT)
  ✓ Hard daily action budgets
  ✓ Random "coffee break" idle periods
  ✓ 2Captcha fallback for unexpected challenges
  ✓ Homepage / feed warm-up before first profile visit
"""

from __future__ import annotations

import asyncio
import json
import random
from dataclasses import dataclass, field
from datetime import timedelta
from pathlib import Path
from typing import Any

from ..compliance.source_policy import get_source_policy
from ..models.source import SourceType
from .device_profile import DeviceProfileManager
from .human_emulator import (
    ActionBudget,
    action_pause,
    between_profiles_pause,
    coffee_break,
    dwell_for_content,
    feed_reading_pause,
    human_click,
    human_scroll,
    human_scroll_with_reversal,
    human_type,
    idle_drift,
    is_weekday,
    post_connect_pause,
    session_start_delay_seconds,
    short_pause,
    simulate_tab_blur,
    within_working_hours,
)
from .session_manager import SessionManager

# ---------------------------------------------------------------------------
# Data model for an extracted LinkedIn profile
# ---------------------------------------------------------------------------


@dataclass
class LinkedInProfile:
    profile_url: str
    full_name: str = ""
    headline: str = ""
    company: str = ""
    location: str = ""
    about: str = ""
    connection_degree: str = ""  # "1st", "2nd", "3rd+"
    has_email: bool = False
    email: str = ""
    skills: list[str] = field(default_factory=list)
    experience: list[dict[str, str]] = field(default_factory=list)
    education: list[dict[str, str]] = field(default_factory=list)
    recent_activity: list[str] = field(default_factory=list)
    raw_html_snippet: str = ""


# ---------------------------------------------------------------------------
# localStorage persistence helpers
# ---------------------------------------------------------------------------


def _storage_path(account_id: str) -> Path:
    return Path("sessions") / f"{account_id}_storage.json"


def _save_storage_state(account_id: str, state: dict) -> None:
    import json as _json

    try:
        _storage_path(account_id).write_text(_json.dumps(state, indent=2))
    except Exception as e:
        print(f"failed to persist storage state for {account_id}: {e}")


def _load_storage_state(account_id: str) -> dict | None:
    import json as _json

    path = _storage_path(account_id)
    if not path.exists():
        return None
    try:
        return _json.loads(path.read_text())
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Main crawler class
# ---------------------------------------------------------------------------


class LinkedInStealthCrawler:
    """
    Scrape LinkedIn profiles slowly and safely using Camoufox.

    Parameters
    ----------
    account_id : str
        The burner account identifier (must have a saved session cookie).
    target_urls : list[str]
        LinkedIn profile URLs to visit.
    captcha_api_key : str | None
        2Captcha API key. If None, CAPTCHA challenges will pause and alert.
    proxy : str | None
        Residential proxy in format "http://user:pass@host:port".
        Strongly recommended for accounts at scale.
    """

    LINKEDIN_HOME = "https://www.linkedin.com/feed/"

    def __init__(
        self,
        account_id: str,
        target_urls: list[str],
        captcha_api_key: str | None = None,
        proxy: str | None = None,
        sessions_dir: str = "sessions",
        tz_offset: int = 5,  # PKT = UTC+5
    ) -> None:
        self.account_id = account_id
        self.target_urls = target_urls
        self.captcha_api_key = captcha_api_key
        self.proxy = proxy
        self.session_manager = SessionManager(sessions_dir)
        self.budget = ActionBudget()
        self.tz_offset = tz_offset

    # Warmup-gated action types -- page_load has no warmup-derived limit
    # (ActionBudget's own flat default applies to it instead), so it's never
    # reserved/released against the session-file ledger.
    _WARMUP_ACTIONS = ("profile_view", "connect", "message", "search")

    def _reserve_daily_budget(self, warmup: dict[str, Any]) -> dict[str, int]:
        """
        Atomically reserves (and immediately logs) this run's share of
        today's remaining warmup allowance for each action type, via
        SessionManager.reserve_action -- the same fix applied to
        OutreachAutomator._reserve_message_budget. Reading
        get_today_limits() and logging usage only after crawling (the
        previous behavior) let two overlapping/sequential linkedin-run
        invocations both see "nothing used yet today" and each get the
        full warmup limit, and logging after the fact could never undo an
        already-completed overage. Returns the granted amount per action
        type; call _release_unused_daily_budget with this same dict once
        the real usage is known.
        """
        return {
            action: self.session_manager.reserve_action(self.account_id, action, warmup[action])
            for action in self._WARMUP_ACTIONS
        }

    def _release_unused_daily_budget(self, reserved: dict[str, int]) -> None:
        for action, granted in reserved.items():
            unused = granted - self.budget._counts.get(action, 0)
            if unused > 0:
                self.session_manager.release_action(self.account_id, action, unused)

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    async def run(self) -> list[LinkedInProfile]:
        """
        Main crawl loop. Returns a list of extracted profiles.
        Respects working hours and daily budgets automatically.
        """
        policy = get_source_policy(SourceType.LINKEDIN)
        print(f"[Crawler] Source policy for LINKEDIN: {policy.authorization_basis.value}")
        print(f"[Crawler] {policy.notes}")

        try:
            from camoufox.async_api import AsyncCamoufox
        except ImportError:
            raise ImportError("camoufox is not installed. Run: pip install 'camoufox[geoip]'")

        if not within_working_hours(self.tz_offset):
            print("[Crawler] Outside working hours (09:00–18:30). Exiting to avoid suspicion.")
            return []

        if not is_weekday():
            print(
                "[Crawler] It's the weekend. LinkedIn activity on weekends raises suspicion. Exiting."
            )
            return []

        if not self.session_manager.has_session(self.account_id):
            raise RuntimeError(
                f"No session found for '{self.account_id}'. "
                "Run the login command first to save your LinkedIn session."
            )

        # A CAPTCHA challenge on ANY prior run (whether started via
        # linkedin-run or the account farm's subprocess worker -- both
        # paths call this same run() method) means this account is
        # "watched" by LinkedIn and must rest, regardless of who reruns
        # it. _check_for_captcha's own docstring already claims a
        # mandatory 24h rest; nothing previously enforced it here.
        cooldown_remaining = self.session_manager.captcha_cooldown_remaining(self.account_id)
        if cooldown_remaining > timedelta(0):
            print(
                f"[Crawler] Account '{self.account_id}' is in CAPTCHA cooldown for another "
                f"{cooldown_remaining}. Skipping this run to avoid a restriction."
            )
            return []

        # Apply warmup limits — override the default ActionBudget limits
        warmup = self.session_manager.get_today_limits(self.account_id)
        print(f"\n[Crawler] Warmup status: {warmup['phase_label']}")
        print(
            f"[Crawler] Today's limits — "
            f"profile_view: {warmup['profile_view']}, "
            f"connect: {warmup['connect']}, "
            f"message: {warmup['message']}\n"
        )

        if warmup["profile_view"] == 0:
            print("[Crawler] Phase 1 (Feed Warmup): No profile visits today.")
            print("[Crawler] Will browse the feed to build account history, then exit.")
            # Use the same device profile as regular runs for consistency
            dpm_phase1 = DeviceProfileManager()
            dev_phase1 = dpm_phase1.get(self.account_id)
            cookies = self.session_manager.load_cookies(self.account_id)
            launch_kw: dict[str, Any] = {"humanize": True, "headless": False, "addons": []}
            if self.proxy:
                launch_kw["proxy"] = {"server": self.proxy}
            async with AsyncCamoufox(**launch_kw) as browser:
                context = await browser.new_context(
                    locale=dev_phase1.locale,
                    timezone_id=dev_phase1.timezone_id,
                    geolocation={
                        "latitude": dev_phase1.geo_latitude,
                        "longitude": dev_phase1.geo_longitude,
                    },
                    permissions=["geolocation"],
                    viewport={
                        "width": dev_phase1.viewport_width,
                        "height": dev_phase1.viewport_height,
                    },
                    screen={"width": dev_phase1.screen_width, "height": dev_phase1.screen_height},
                    user_agent=dev_phase1.user_agent,
                )
                await context.add_cookies(cookies)
                page = await context.new_page()
                await self._warm_up_feed(page)
                updated = await context.cookies()
                await context.close()
            self.session_manager.save_cookies(self.account_id, updated)
            self.session_manager.log_run(self.account_id, {"feed_scroll": 1})
            print("[Crawler] Feed warmup complete. Come back tomorrow to continue.")
            return []

        # Reserve today's remaining warmup allowance atomically (see
        # _reserve_daily_budget) instead of handing this run the FULL daily
        # warmup limit regardless of what an earlier invocation already
        # used today -- two sequential (or overlapping) linkedin-run
        # invocations for the same account could otherwise each visit the
        # full daily quota, since logging only happened after crawling
        # finished. reserved[...] already accounts for today's prior usage,
        # so it becomes this run's entire DAILY_LIMITS for these actions.
        reserved = self._reserve_daily_budget(warmup)
        self.budget.DAILY_LIMITS = {**self.budget.DAILY_LIMITS, **reserved}

        # Wraps EVERYTHING from the reservation above onward -- cookie
        # loading, the device profile lookup, the preferred-start-time
        # delay, and browser launch/context setup -- not just the
        # established browser session's own cleanup (the inner finally
        # below). A corrupt session file, a cancelled delay, or a
        # browser-launch failure previously skipped the release entirely,
        # since none of those failures ever reached that inner finally,
        # consuming the account's whole remaining daily quota for zero
        # actions and blocking every later run until the next day.
        try:
            cookies = self.session_manager.load_cookies(self.account_id)
            results: list[LinkedInProfile] = []

            # Load consistent device profile for this account
            dpm = DeviceProfileManager()
            device = dpm.get(self.account_id)

            # Respect preferred session start time (avoids identical daily start patterns)
            delay_secs = session_start_delay_seconds(
                device.preferred_start_hour,
                device.preferred_start_jitter,
            )
            if delay_secs > 60:
                print(
                    f"[Crawler] Waiting {delay_secs / 60:.1f} min before starting "
                    f"(preferred start: ~{device.preferred_start_hour}:00 PKT)..."
                )
                await asyncio.sleep(delay_secs)

            # Camoufox: Firefox-based, patches at engine level
            # humanize=True adds further mouse/timing randomisation at the engine level
            launch_kwargs: dict[str, Any] = {"humanize": True, "headless": False, "addons": []}
            if self.proxy:
                launch_kwargs["proxy"] = {"server": self.proxy}

            async with AsyncCamoufox(**launch_kwargs) as browser:
                context = await browser.new_context(
                    locale=device.locale,
                    timezone_id=device.timezone_id,
                    geolocation={
                        "latitude": device.geo_latitude,
                        "longitude": device.geo_longitude,
                    },
                    permissions=["geolocation"],
                    viewport={"width": device.viewport_width, "height": device.viewport_height},
                    screen={"width": device.screen_width, "height": device.screen_height},
                    user_agent=device.user_agent,
                    extra_http_headers={
                        "Accept-Language": device.accept_language,
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                        "Sec-Ch-Ua-Platform": '"Windows"',
                        "Upgrade-Insecure-Requests": "1",
                    },
                )

                # Inject saved session cookies
                await context.add_cookies(cookies)

                # Create the page FIRST, then restore localStorage
                # (localStorage can only be set after a page exists and has navigated)
                page = await context.new_page()

                stored_state = _load_storage_state(self.account_id)
                if stored_state:
                    await page.goto("https://www.linkedin.com", wait_until="domcontentloaded")
                    await page.evaluate(f"""
                        const state = {json.dumps(stored_state)};
                        for (const [k, v] of Object.entries(state.localStorage || {{}})) {{
                            try {{ localStorage.setItem(k, v); }} catch(e) {{}}
                        }}
                    """)

                # Inject JS to track mouse position AND override hardware/device signals
                await page.add_init_script(f"""
                    // Mouse position tracker (used by human_move_to)
                    window.mouseX = 0;
                    window.mouseY = 0;
                    document.addEventListener('mousemove', e => {{
                        window.mouseX = e.clientX;
                        window.mouseY = e.clientY;
                    }});

                    // Override hardware concurrency (CPU cores)
                    Object.defineProperty(navigator, 'hardwareConcurrency', {{
                        get: () => {device.hardware_concurrency}
                    }});

                    // Override device memory
                    Object.defineProperty(navigator, 'deviceMemory', {{
                        get: () => {device.device_memory}
                    }});

                    // Override platform
                    Object.defineProperty(navigator, 'platform', {{
                        get: () => '{device.platform}'
                    }});

                    // Disable WebRTC to prevent real IP leaks
                    if (window.RTCPeerConnection) {{
                        window.RTCPeerConnection = undefined;
                    }}
                    if (window.webkitRTCPeerConnection) {{
                        window.webkitRTCPeerConnection = undefined;
                    }}

                    // Canvas fingerprint noise (consistent per account)
                    const _toDataURL = HTMLCanvasElement.prototype.toDataURL;
                    HTMLCanvasElement.prototype.toDataURL = function(type) {{
                        const seed = {device.canvas_noise_seed};
                        const ctx = this.getContext('2d');
                        if (ctx) {{
                            const pixel = ctx.getImageData(0, 0, 1, 1);
                            pixel.data[0] = (pixel.data[0] + seed % 5) % 256;
                            ctx.putImageData(pixel, 0, 0);
                        }}
                        return _toDataURL.apply(this, arguments);
                    }};
                """)

                try:
                    await self._warm_up_feed(page)

                    for url in self.target_urls:
                        if not within_working_hours(self.tz_offset):
                            print("[Crawler] Reached end of working hours. Stopping gracefully.")
                            break

                        try:
                            self.budget.charge("profile_view")
                        except RuntimeError as e:
                            print(f"[Crawler] {e}")
                            break

                        print(f"[Crawler] Visiting: {url} | Budget: {self.budget.summary()}")

                        # Occasionally navigate via search instead of direct URL
                        # This makes the navigation graph look human
                        if random.random() < 0.40:
                            profile = await self._visit_via_search(page, url)
                        else:
                            profile = await self._visit_profile(page, url)
                        if profile:
                            results.append(profile)
                            print(f"[Crawler] ✓ Extracted: {profile.full_name} @ {profile.company}")

                        # Occasionally idle drift and/or simulate tab switch
                        if random.random() < 0.20:
                            await idle_drift(page)
                        if random.random() < 0.15:
                            await simulate_tab_blur(page)

                        # Occasionally take a coffee break (1 in 8 profiles)
                        if random.random() < 0.12:
                            print("[Crawler] Taking a coffee break...")
                            await coffee_break()
                        else:
                            await between_profiles_pause()

                except Exception as e:
                    # A CAPTCHA-triggered abort (_check_for_captcha's own
                    # intentional RuntimeError), a search-budget exhaustion,
                    # or any other browser-level failure previously escaped
                    # this method entirely once earlier URLs had already
                    # succeeded -- run() never reached `return results`, so
                    # cli.py's linkedin_run never reached its persistence
                    # block, and account_farm.py's worker caught the
                    # exception and explicitly returned an empty profile
                    # list, discarding every profile harvested before the
                    # abort. Attach what was collected so far to the
                    # exception (still re-raised as-is, so anything
                    # matching its type/message elsewhere is unaffected)
                    # and let callers decide how to persist it.
                    e.partial_profiles = results
                    raise
                finally:
                    # Save cookies AND localStorage back to disk
                    updated_cookies = await context.cookies()
                    local_storage = await page.evaluate("""
                        () => {
                            const s = {};
                            for (let i = 0; i < localStorage.length; i++) {
                                const k = localStorage.key(i);
                                s[k] = localStorage.getItem(k);
                            }
                            return s;
                        }
                    """)
                    self.session_manager.save_cookies(self.account_id, updated_cookies)
                    _save_storage_state(self.account_id, {"localStorage": local_storage})
                    await context.close()
        finally:
            # reserve_action already logged the full `reserved` amount up
            # front (see _reserve_daily_budget) so a concurrent run sees it
            # immediately -- give back whatever portion of that reservation
            # this run didn't actually use. In the outer finally (not the
            # inner one above) so it still runs even when a failure
            # happens before the browser session is ever established --
            # see the comment where `reserved` is assigned.
            self._release_unused_daily_budget(reserved)

        print(f"[Crawler] Done. Extracted {len(results)} profiles.")
        return results

    # ------------------------------------------------------------------
    # Feed warm-up — simulate a human checking their feed first
    # ------------------------------------------------------------------

    async def _visit_via_search(self, page: Any, target_url: str) -> LinkedInProfile | None:
        """
        Navigate to a profile via LinkedIn search instead of direct URL.
        This mimics how a real recruiter finds someone, making the navigation
        graph look human rather than a direct URL injection sequence.
        """
        try:
            # Extract the profile slug to build a name-based search query
            slug = target_url.rstrip("/").split("/in/")[-1].replace("-", " ")
            search_query = slug[:40]  # truncate for natural search length

            self.budget.charge("search")
            search_url = f"https://www.linkedin.com/search/results/people/?keywords={search_query.replace(' ', '%20')}"
            await page.goto(search_url, wait_until="networkidle", timeout=30_000)
            await self._check_for_captcha(page)
            await action_pause()

            # Scroll results as if reading them
            await human_scroll_with_reversal(page, "down", 2)
            await asyncio.sleep(random.uniform(3, 8))

            # Try to click on the matching result
            results = await page.query_selector_all(".reusable-search__result-container")
            for result in results[:5]:
                link = await result.query_selector("a[href*='/in/']")
                if link:
                    href = await link.get_attribute("href") or ""
                    # Check if the slug matches our target
                    slug_fragment = target_url.rstrip("/").split("/in/")[-1].split("?")[0]
                    if slug_fragment.lower() in href.lower():
                        await link.click()
                        await page.wait_for_load_state("networkidle", timeout=15_000)
                        await self._check_for_captcha(page)
                        await dwell_for_content(page)
                        return await self._extract_profile(page, page.url)

            # Fallback: direct visit if search didn't find exact match
            return await self._visit_profile(page, target_url)

        except RuntimeError:
            raise
        except Exception as e:
            print(f"[Crawler] Search-based visit failed ({e}), falling back to direct.")
            return await self._visit_profile(page, target_url)

    async def _warm_up_feed(self, page: Any) -> None:
        """Visit the feed, scroll around, simulate reading before visiting profiles."""
        print("[Crawler] Warming up — reading the LinkedIn feed...")
        self.budget.charge("page_load")
        await page.goto(self.LINKEDIN_HOME, wait_until="networkidle", timeout=30_000)
        await self._check_for_captcha(page)

        # Scroll the feed naturally, as if reading
        for _ in range(random.randint(2, 5)):
            await human_scroll(page, "down", random.randint(2, 5))
            await asyncio.sleep(random.uniform(3, 12))

        await feed_reading_pause()

    # ------------------------------------------------------------------
    # Visit a single profile
    # ------------------------------------------------------------------

    async def _visit_profile(self, page: Any, url: str) -> LinkedInProfile | None:
        try:
            self.budget.charge("page_load")
            await page.goto(url, wait_until="networkidle", timeout=30_000)
            await self._check_for_captcha(page)
            await action_pause()

            # Scroll through the profile naturally
            await human_scroll(page, "down", random.randint(3, 6))
            await asyncio.sleep(random.uniform(5, 15))
            await human_scroll(page, "down", random.randint(2, 4))
            await asyncio.sleep(random.uniform(3, 10))

            return await self._extract_profile(page, url)

        except RuntimeError:
            raise  # Budget exhausted — propagate upward
        except Exception as e:
            print(f"[Crawler] ✗ Failed to visit {url}: {e}")
            return None

    # ------------------------------------------------------------------
    # Data extraction (DOM scraping)
    # ------------------------------------------------------------------

    async def _extract_profile(self, page: Any, url: str) -> LinkedInProfile:
        profile = LinkedInProfile(profile_url=url)

        try:
            profile.full_name = await self._safe_text(page, "h1.text-heading-xlarge")
            profile.headline = await self._safe_text(page, ".text-body-medium.break-words")
            profile.location = await self._safe_text(
                page, ".text-body-small.inline.t-black--light.break-words"
            )
            profile.connection_degree = await self._safe_text(page, ".dist-value")

            # About section (click "see more" if present)
            try:
                see_more = await page.query_selector(
                    "#about ~ .pvs-list__outer-container .inline-show-more-text__button"
                )
                if see_more:
                    await see_more.click()
                    await short_pause()
            except Exception as e:
                # Best-effort UI interaction -- the "see more" button may not
                # be present or LinkedIn's DOM structure may have shifted;
                # the About section is simply left as-is.
                print(f"'see more' click skipped while scraping about section: {e}")
            profile.about = await self._safe_text(page, "#about ~ .pvs-list__outer-container")

            # Experience (top entry only to keep things light)
            exp_items = await page.query_selector_all(
                "#experience ~ .pvs-list__outer-container .pvs-list__item--line-separated"
            )
            for item in exp_items[:3]:
                title = await self._safe_text_el(item, ".t-bold .visually-hidden")
                company = await self._safe_text_el(item, ".t-14.t-normal .visually-hidden")
                if title:
                    profile.experience.append({"title": title, "company": company})
                    if not profile.company:
                        profile.company = company

            # Education (top entry)
            edu_items = await page.query_selector_all(
                "#education ~ .pvs-list__outer-container .pvs-list__item--line-separated"
            )
            for item in edu_items[:2]:
                school = await self._safe_text_el(item, ".t-bold .visually-hidden")
                degree = await self._safe_text_el(item, ".t-14.t-normal .visually-hidden")
                if school:
                    profile.education.append({"school": school, "degree": degree})

            # Recent activity (post snippets)
            activity_items = await page.query_selector_all(".feed-shared-update-v2__description")
            for item in activity_items[:3]:
                text = (await item.inner_text()).strip()
                if text:
                    profile.recent_activity.append(text[:300])

            # Grab HTML snippet for AI research
            snippet_el = await page.query_selector("main")
            if snippet_el:
                profile.raw_html_snippet = (await snippet_el.inner_text())[:3000]

        except Exception as e:
            print(f"[Crawler] Extraction warning for {url}: {e}")

        return profile

    # ------------------------------------------------------------------
    # Connection request
    # ------------------------------------------------------------------

    async def send_connection_request(
        self,
        page: Any,
        profile_url: str,
        note: str = "",
    ) -> bool:
        """
        Navigate to a profile and send a connection request with an
        optional personalised note.
        Returns True if successful.
        """
        try:
            self.budget.charge("connect")
        except RuntimeError as e:
            print(f"[Crawler] {e}")
            return False

        try:
            await page.goto(profile_url, wait_until="networkidle", timeout=30_000)
            await self._check_for_captcha(page)
            await action_pause()
            await human_scroll(page, "down", 1)
            await asyncio.sleep(random.uniform(4, 12))

            # Find the Connect button
            connect_btn = await page.query_selector("button[aria-label*='Connect']")
            if not connect_btn:
                # Might be under "More" menu
                more_btn = await page.query_selector("button[aria-label='More actions']")
                if more_btn:
                    await human_click(page, "button[aria-label='More actions']")
                    await short_pause()
                    connect_btn = await page.query_selector("[aria-label*='Connect']")

            if not connect_btn:
                print(f"[Crawler] No Connect button found on {profile_url}")
                return False

            await connect_btn.click()
            await action_pause()

            # Add a personalised note if provided
            if note:
                add_note_btn = await page.query_selector("button[aria-label='Add a note']")
                if add_note_btn:
                    await add_note_btn.click()
                    await short_pause()
                    await human_type(page, "textarea[name='message']", note)
                    await action_pause()

            # Click Send
            send_btn = await page.query_selector(
                "button[aria-label='Send now']"
            ) or await page.query_selector("button[aria-label='Send invitation']")
            if send_btn:
                await send_btn.click()
                print(f"[Crawler] ✓ Connection request sent to {profile_url}")
                await post_connect_pause()
                return True

        except Exception as e:
            print(f"[Crawler] ✗ Failed to send connection to {profile_url}: {e}")

        return False

    # ------------------------------------------------------------------
    # Direct message (1st degree connections only)
    # ------------------------------------------------------------------

    async def send_message(
        self,
        page: Any,
        profile_url: str,
        message: str,
    ) -> bool:
        """Send a direct message to a 1st-degree connection."""
        try:
            self.budget.charge("message")
        except RuntimeError as e:
            print(f"[Crawler] {e}")
            return False

        try:
            await page.goto(profile_url, wait_until="networkidle", timeout=30_000)
            await self._check_for_captcha(page)
            await action_pause()

            msg_btn = await page.query_selector("button[aria-label*='Message']")
            if not msg_btn:
                print(
                    f"[Crawler] No Message button — likely not a 1st-degree connection: {profile_url}"
                )
                return False

            await msg_btn.click()
            await action_pause()

            # Type the message naturally
            await human_type(page, ".msg-form__contenteditable", message)
            await action_pause()

            # Send
            send_btn = await page.query_selector("button.msg-form__send-button")
            if send_btn:
                await send_btn.click()
                print(f"[Crawler] ✓ Message sent to {profile_url}")
                await post_connect_pause()
                return True

        except Exception as e:
            print(f"[Crawler] ✗ Failed to message {profile_url}: {e}")

        return False

    # ------------------------------------------------------------------
    # CAPTCHA handling
    # ------------------------------------------------------------------

    async def _check_for_captcha(self, page: Any) -> None:
        """
        Detect a CAPTCHA and either solve it via 2Captcha or pause and alert.

        IMPORTANT — Challenge Binding Rule:
        A CAPTCHA appearing means LinkedIn has flagged this session.
        Even if we solve it successfully, the session is now 'watched'.
        We ALWAYS enforce a 24-hour rest after any challenge appears.
        The solved token is bound to this exact session + page — never reuse it.
        """
        try:
            captcha_el = await page.query_selector(
                "iframe[src*='captcha'], #captcha-challenge, .captcha__image"
            )
            if not captcha_el:
                return

            print("⚠ [Crawler] CAPTCHA detected — session is flagged by LinkedIn!")

            # Log CAPTCHA event to session (audit trail) and the exact
            # timestamp run()'s own captcha_cooldown_remaining check reads
            # to actually enforce the claimed 24h rest before this account
            # is used again -- log_run alone previously had nothing reading
            # it back. Recorded immediately, before attempting a solve: the
            # challenge is already definitively detected at this point
            # regardless of whether solving it below succeeds, times out,
            # or raises, so the cooldown must not depend on reaching the
            # code after the solve attempt.
            self.session_manager.log_run(self.account_id, {"captcha_triggered": 1})
            self.session_manager.record_captcha_challenge(self.account_id)

            if self.captcha_api_key:
                await self._solve_captcha_2captcha(page)
            else:
                print("[Crawler] No 2Captcha key. Pausing 5 min for manual solve...")
                await asyncio.sleep(300)

            # Raise to abort remaining URLs — account needs 24h rest regardless of solve outcome
            raise RuntimeError(
                f"CaptchaTriggered:{self.account_id} — enforcing 24-hour account rest. "
                "Do not run this account again until tomorrow."
            )

        except RuntimeError:
            raise  # Propagate the rest-enforcement signal upward
        except Exception as e:
            # If CAPTCHA/checkpoint detection itself fails, proceed cautiously
            # rather than aborting the whole crawl over a detection-logic bug.
            print(f"CAPTCHA/checkpoint detection failed, proceeding cautiously: {e}")

    async def _solve_captcha_2captcha(self, page: Any) -> None:
        """Attempt to solve a CAPTCHA using the 2Captcha API."""
        try:
            from twocaptcha import TwoCaptcha

            solver = TwoCaptcha(self.captcha_api_key)

            page_url = page.url

            # Try reCAPTCHA v2
            sitekey_el = await page.query_selector("[data-sitekey]")
            if sitekey_el:
                sitekey = await sitekey_el.get_attribute("data-sitekey")
                print(f"[2Captcha] Solving reCAPTCHA v2 (sitekey: {sitekey[:12]}...)...")
                result = solver.recaptcha(sitekey=sitekey, url=page_url)
                token = result.get("code", "")
                if token:
                    await page.evaluate(
                        f'document.getElementById("g-recaptcha-response").innerHTML = "{token}";'
                    )
                    await page.evaluate(
                        "___grecaptcha_cfg.clients[0].aa.l.callback('" + token + "')"
                    )
                    await asyncio.sleep(3)
                    print("[2Captcha] ✓ reCAPTCHA solved.")
                    return

            print("[2Captcha] Could not identify CAPTCHA type. Pausing for manual solve...")
            await asyncio.sleep(120)

        except Exception as e:
            print(f"[2Captcha] Solver failed: {e}. Pausing for manual solve...")
            await asyncio.sleep(120)

    # ------------------------------------------------------------------
    # DOM helper utilities
    # ------------------------------------------------------------------

    @staticmethod
    async def _safe_text(page: Any, selector: str) -> str:
        try:
            el = await page.query_selector(selector)
            return (await el.inner_text()).strip() if el else ""
        except Exception:
            return ""

    @staticmethod
    async def _safe_text_el(element: Any, selector: str) -> str:
        try:
            el = await element.query_selector(selector)
            return (await el.inner_text()).strip() if el else ""
        except Exception:
            return ""
