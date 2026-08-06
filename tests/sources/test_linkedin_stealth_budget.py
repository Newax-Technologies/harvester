import json
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest

from lead_harvester.sources.linkedin_stealth import LinkedInStealthCrawler
from lead_harvester.sources.session_manager import SessionManager


def _crawler(tmp_path, account_id: str) -> LinkedInStealthCrawler:
    return LinkedInStealthCrawler(account_id=account_id, target_urls=[], sessions_dir=str(tmp_path))


def _backdate_to_week3(tmp_path, account_id: str) -> None:
    # Week 3 limits: profile_view=8, connect=3, message=2, search=10.
    sm = SessionManager(tmp_path)
    sm.save_cookies(account_id, [{"name": "x", "value": "y"}], first_login=True)
    path = tmp_path / f"{account_id}.json"
    payload = json.loads(path.read_text())
    payload["warmup_started_at"] = (datetime.now(UTC).date() - timedelta(days=18)).isoformat()
    path.write_text(json.dumps(payload))


def test_reserve_daily_budget_accounts_for_todays_prior_usage(tmp_path):
    _backdate_to_week3(tmp_path, "burner_01")
    sm = SessionManager(tmp_path)
    # Simulate an earlier run today that already used 5 of the 8 profile
    # views and all 3 connects.
    sm.log_run(
        "burner_01",
        {"profile_view": 5, "connect": 3, "message": 0, "search": 2},
    )

    crawler = _crawler(tmp_path, "burner_01")
    warmup = crawler.session_manager.get_today_limits("burner_01")
    reserved = crawler._reserve_daily_budget(warmup)

    assert reserved == {"profile_view": 3, "connect": 0, "message": 2, "search": 8}


def test_reserve_daily_budget_never_over_grants_across_two_crawler_instances(tmp_path):
    # Previously each LinkedInStealthCrawler.run() invocation applied the
    # FULL warmup limit regardless of another invocation's usage today,
    # since usage was only logged after crawling finished -- two
    # sequential (or overlapping) runs could each visit the full daily
    # quota. Constructing two crawlers for the same account and reserving
    # in sequence must show the second reservation already reduced by the
    # first's.
    _backdate_to_week3(tmp_path, "burner_02")

    first = _crawler(tmp_path, "burner_02")
    second = _crawler(tmp_path, "burner_02")

    warmup = first.session_manager.get_today_limits("burner_02")
    first_reserved = first._reserve_daily_budget(warmup)
    second_reserved = second._reserve_daily_budget(warmup)

    assert first_reserved == {"profile_view": 8, "connect": 3, "message": 2, "search": 10}
    assert second_reserved == {"profile_view": 0, "connect": 0, "message": 0, "search": 0}


def test_release_unused_daily_budget_gives_back_unused_portion(tmp_path):
    _backdate_to_week3(tmp_path, "burner_03")
    crawler = _crawler(tmp_path, "burner_03")
    warmup = crawler.session_manager.get_today_limits("burner_03")

    reserved = crawler._reserve_daily_budget(warmup)
    assert reserved["profile_view"] == 8

    # Only 3 of the 8 reserved profile views were actually used.
    crawler.budget._counts["profile_view"] = 3
    crawler._release_unused_daily_budget(reserved)

    # A fresh reservation attempt should see 5 profile views given back.
    second = _crawler(tmp_path, "burner_03")
    second_reserved = second._reserve_daily_budget(warmup)
    assert second_reserved["profile_view"] == 5


@pytest.mark.asyncio
async def test_run_skips_account_still_in_captcha_cooldown(tmp_path, monkeypatch):
    # _check_for_captcha's own docstring claims a mandatory 24-hour rest
    # after any challenge, regardless of solve outcome -- but nothing
    # previously read that logged event back before starting the account
    # again. run() must refuse to even open a browser while the cooldown
    # from a prior challenge is still active.
    from lead_harvester.config import settings

    monkeypatch.setattr(settings, "restricted_sources_enabled", True)

    _backdate_to_week3(tmp_path, "burner_07")
    sm = SessionManager(tmp_path)
    sm.record_captcha_challenge("burner_07")

    crawler = _crawler(tmp_path, "burner_07")

    with (
        patch("lead_harvester.sources.linkedin_stealth.within_working_hours", return_value=True),
        patch("lead_harvester.sources.linkedin_stealth.is_weekday", return_value=True),
    ):
        result = await crawler.run()

    assert result == []
