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
async def test_run_attaches_partial_profiles_when_the_loop_aborts(tmp_path):
    # A CAPTCHA-triggered abort (_check_for_captcha's own intentional
    # RuntimeError), a search-budget exhaustion, or any other browser-level
    # failure after earlier URLs already succeeded previously discarded
    # every profile harvested so far -- run() never reached `return
    # results` at all, so cli.py's linkedin_run never reached its
    # persistence block and account_farm.py's worker explicitly returned
    # an empty profile list.
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
