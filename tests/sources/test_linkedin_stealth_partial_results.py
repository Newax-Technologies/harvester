import json
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, patch

import pytest

from lead_harvester.sources.linkedin_stealth import LinkedInProfile, LinkedInStealthCrawler
from lead_harvester.sources.session_manager import SessionManager


def _backdate_to_week3(tmp_path, account_id: str) -> None:
    # Week 3 limits: profile_view=8, connect=3, message=2, search=10 -- a
    # freshly created (Day 1, Phase 1) account has profile_view=0 and would
    # hit run()'s early "feed warmup only" return before ever reaching the
    # crawl loop.
    sm = SessionManager(tmp_path)
    sm.save_cookies(account_id, [{"name": "x", "value": "y"}], first_login=True)
    path = tmp_path / f"{account_id}.json"
    payload = json.loads(path.read_text())
    payload["warmup_started_at"] = (datetime.now(UTC).date() - timedelta(days=18)).isoformat()
    path.write_text(json.dumps(payload))


class _FakeAsyncCamoufox:
    def __init__(self, browser, **kwargs):
        self._browser = browser

    async def __aenter__(self):
        return self._browser

    async def __aexit__(self, *args):
        return False


def _fake_browser():
    page = AsyncMock()
    page.evaluate = AsyncMock(return_value={})
    page.goto = AsyncMock()

    context = AsyncMock()
    context.new_page = AsyncMock(return_value=page)
    context.add_cookies = AsyncMock()
    context.cookies = AsyncMock(return_value=[])
    context.close = AsyncMock()

    browser = AsyncMock()
    browser.new_context = AsyncMock(return_value=context)
    return browser


@pytest.mark.asyncio
async def test_run_attaches_partial_profiles_when_the_loop_aborts(tmp_path, monkeypatch):
    # A CAPTCHA-triggered abort (_check_for_captcha's own intentional
    # RuntimeError), a search-budget exhaustion, or any other browser-level
    # failure after earlier URLs already succeeded previously discarded
    # every profile harvested so far -- run() never reached `return
    # results` at all, so cli.py's linkedin_run never reached its
    # persistence block and account_farm.py's worker explicitly returned
    # an empty profile list.
    from lead_harvester.config import settings

    monkeypatch.setattr(settings, "restricted_sources_enabled", True)

    _backdate_to_week3(tmp_path, "burner_partial")
    crawler = LinkedInStealthCrawler(
        account_id="burner_partial",
        target_urls=["https://linkedin.com/in/alice", "https://linkedin.com/in/bob"],
        sessions_dir=str(tmp_path),
    )

    good_profile = LinkedInProfile(profile_url="https://linkedin.com/in/alice", full_name="Alice")
    crawler._visit_profile = AsyncMock(
        side_effect=[good_profile, RuntimeError("CaptchaTriggered:burner_partial")]
    )
    crawler._visit_via_search = AsyncMock()
    crawler._warm_up_feed = AsyncMock()

    browser = _fake_browser()

    with (
        patch("lead_harvester.sources.linkedin_stealth.within_working_hours", return_value=True),
        patch("lead_harvester.sources.linkedin_stealth.is_weekday", return_value=True),
        # Forces the direct-visit branch (never _visit_via_search) and skips
        # the occasional idle-drift/tab-blur/coffee-break random detours.
        patch("lead_harvester.sources.linkedin_stealth.random.random", return_value=0.99),
        patch(
            "lead_harvester.sources.linkedin_stealth.between_profiles_pause",
            new=AsyncMock(),
        ),
        # "burner_partial"'s deterministically-seeded DeviceProfile happens
        # to produce a preferred-start delay of several real minutes --
        # unmocked, run() actually awaits asyncio.sleep(delay_secs) for that
        # long before ever reaching the crawl loop this test cares about,
        # the same real-timing risk between_profiles_pause above is already
        # mocked away for.
        patch(
            "lead_harvester.sources.linkedin_stealth.session_start_delay_seconds",
            return_value=0,
        ),
        patch(
            "camoufox.async_api.AsyncCamoufox",
            lambda **kwargs: _FakeAsyncCamoufox(browser, **kwargs),
        ),
        pytest.raises(RuntimeError, match="CaptchaTriggered") as exc_info,
    ):
        await crawler.run()

    partial_profiles = exc_info.value.partial_profiles
    assert len(partial_profiles) == 1
    assert partial_profiles[0].full_name == "Alice"

    # Regression: run() previously constructed DeviceProfileManager() with
    # no arguments, silently defaulting to the module-level "sessions"
    # directory regardless of the sessions_dir this crawler was configured
    # with -- persisting a real device-fingerprint file into the repo's
    # cwd-relative "sessions/" folder on every test run instead of tmp_path.
    assert (tmp_path / "burner_partial_device.json").exists()
    assert not (tmp_path / "sessions").exists()
