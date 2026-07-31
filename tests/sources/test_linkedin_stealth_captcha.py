from unittest.mock import AsyncMock

import pytest

from lead_harvester.sources.linkedin_stealth import LinkedInStealthCrawler
from lead_harvester.sources.session_manager import SessionManager


class _FakeElement:
    async def get_attribute(self, name):
        return "fake-sitekey"


class _FakePage:
    """Reports a CAPTCHA present on the very first query_selector call."""

    def __init__(self):
        self.url = "https://www.linkedin.com/checkpoint/challenge"

    async def query_selector(self, selector):
        return _FakeElement()


def _crawler(tmp_path, account_id: str = "burner_captcha") -> LinkedInStealthCrawler:
    crawler = LinkedInStealthCrawler(
        account_id=account_id, target_urls=[], sessions_dir=str(tmp_path)
    )
    crawler.session_manager.save_cookies(
        account_id, [{"name": "x", "value": "y"}], first_login=True
    )
    return crawler


@pytest.mark.asyncio
async def test_captcha_cooldown_recorded_even_when_solver_raises(tmp_path):
    # The challenge is definitively detected the moment captcha_el is found
    # -- the cooldown must be persisted immediately, not only after a solve
    # attempt that could time out, get rejected, or raise. A non-RuntimeError
    # from the solver (e.g. a 2Captcha client's own exception type) is
    # swallowed by _check_for_captcha's generic except-and-continue handler
    # (unchanged, pre-existing behavior -- detection-logic failures must not
    # abort the whole crawl), so no exception propagates here; what matters
    # is that the cooldown was already recorded before that solve attempt.
    crawler = _crawler(tmp_path)
    crawler.captcha_api_key = "fake-2captcha-key"
    crawler._solve_captcha_2captcha = AsyncMock(side_effect=TimeoutError("2Captcha timed out"))

    await crawler._check_for_captcha(_FakePage())

    sm = SessionManager(tmp_path)
    assert sm.captcha_cooldown_remaining("burner_captcha").total_seconds() > 0


@pytest.mark.asyncio
async def test_captcha_cooldown_recorded_without_api_key(tmp_path, monkeypatch):
    # No captcha_api_key configured -- falls back to the manual-solve pause,
    # which must still record the cooldown immediately.
    crawler = _crawler(tmp_path)
    assert crawler.captcha_api_key is None

    async def _no_sleep(*args, **kwargs):
        return None

    monkeypatch.setattr("lead_harvester.sources.linkedin_stealth.asyncio.sleep", _no_sleep)

    with pytest.raises(RuntimeError, match="CaptchaTriggered"):
        await crawler._check_for_captcha(_FakePage())

    sm = SessionManager(tmp_path)
    assert sm.captcha_cooldown_remaining("burner_captcha").total_seconds() > 0
