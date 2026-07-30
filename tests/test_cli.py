import argparse
import contextlib
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.sources.linkedin_stealth import LinkedInProfile


@contextlib.asynccontextmanager
async def _fake_get_session(session: AsyncSession):
    yield session


@pytest.mark.asyncio
async def test_linkedin_run_constructs_crawler_without_unsupported_kwargs(tmp_path, db_session):
    # linkedin_run previously passed addons=[] to LinkedInStealthCrawler,
    # whose __init__ only accepts account_id, target_urls, captcha_api_key,
    # proxy, sessions_dir, and tz_offset -- every invocation raised
    # TypeError before opening a browser or scraping a single profile.
    from lead_harvester import cli

    urls_file = tmp_path / "urls.txt"
    urls_file.write_text("https://linkedin.com/in/alice\n")

    args = argparse.Namespace(
        account="burner_01",
        urls_file=str(urls_file),
        proxy="",
        captcha_key="",
    )

    fake_profile = LinkedInProfile(profile_url="https://linkedin.com/in/alice", full_name="Alice")

    with (
        patch("lead_harvester.sources.linkedin_stealth.LinkedInStealthCrawler") as mock_crawler_cls,
        patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)),
    ):
        mock_crawler_cls.return_value.run = AsyncMock(return_value=[fake_profile])
        result = await cli.linkedin_run(args)

    assert result == 0
    mock_crawler_cls.assert_called_once_with(
        account_id="burner_01",
        target_urls=["https://linkedin.com/in/alice"],
        captcha_api_key=None,
        proxy=None,
    )
