import argparse
import contextlib
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.source import RawSourceRecord, SourceType
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


@pytest.mark.asyncio
async def test_import_authorized_returns_error_for_missing_file(tmp_path):
    from lead_harvester import cli

    args = argparse.Namespace(
        file=str(tmp_path / "does-not-exist.csv"),
        source_reference="license-2026",
        country_code="",
    )

    result = await cli.import_authorized(args)

    assert result == 1


@pytest.mark.asyncio
async def test_import_authorized_runs_pipeline_with_csv_and_source_reference(tmp_path, db_session):
    from lead_harvester import cli

    csv_path = tmp_path / "leads.csv"
    csv_path.write_text("institution_name,contact_value\nBeacon House School,+923001234567\n")

    args = argparse.Namespace(
        file=str(csv_path),
        source_reference="license-2026-education-directory",
        country_code="",
    )

    with patch(
        "lead_harvester.pipeline.get_session",
        new=lambda: _fake_get_session(db_session),
    ):
        result = await cli.import_authorized(args)

    assert result == 0

    records = (
        (
            await db_session.execute(
                select(RawSourceRecord).where(
                    RawSourceRecord.source_type == SourceType.AUTHORIZED_IMPORT
                )
            )
        )
        .scalars()
        .all()
    )
    assert len(records) == 1
    assert records[0].raw_payload["source_reference"] == "license-2026-education-directory"


@pytest.mark.asyncio
async def test_linkedin_farm_run_aborts_when_proxies_file_missing(tmp_path):
    # An operator explicitly supplying --proxies-file wants every account
    # launched behind a residential proxy -- silently continuing with an
    # empty proxy map would launch every burner account from the host's
    # real IP, exposing and correlating "isolated" accounts by shared
    # origin, exactly what the proxy was meant to prevent.
    from lead_harvester import cli

    urls_file = tmp_path / "urls.txt"
    urls_file.write_text("https://linkedin.com/in/alice\n")

    args = argparse.Namespace(
        accounts="burner_01",
        urls_file=str(urls_file),
        proxies_file=str(tmp_path / "does-not-exist-proxies.txt"),
        captcha_key="",
    )

    result = await cli._linkedin_farm_run(args)

    assert result == 1
