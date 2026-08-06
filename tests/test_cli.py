import argparse
import contextlib
import uuid
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.source import RawSourceRecord, SourceType
from lead_harvester.models.tenancy import DEFAULT_TENANT_ID
from lead_harvester.sources.account_farm import AccountResult
from lead_harvester.sources.linkedin_stealth import LinkedInProfile


@contextlib.asynccontextmanager
async def _fake_get_session(session: AsyncSession):
    yield session


@pytest.fixture
def _restricted_sources_enabled(monkeypatch):
    # docs/ROADMAP.md Module 28: LinkedIn account automation is disabled by
    # default (Settings.restricted_sources_enabled=False). Tests below that
    # exercise the mocked crawler/farm's own behavior represent an
    # explicitly approved, non-production environment where the operator
    # has turned it on -- separate from the dedicated gate tests, which
    # prove the default-disabled state actually blocks these commands.
    from lead_harvester.config import settings

    monkeypatch.setattr(settings, "restricted_sources_enabled", True)


@pytest.fixture(autouse=True)
def _clear_provider_credential_env(monkeypatch):
    # run_command's validation guard reads these from Settings(), which
    # falls back to real OS/`.env` values -- clearing them here keeps the
    # guard tests below deterministic regardless of what's set outside the
    # test process.
    for key in (
        "GOOGLE_PLACES_API_KEY",
        "APPLE_MAPS_TEAM_ID",
        "APPLE_MAPS_KEY_ID",
        "APPLE_MAPS_PRIVATE_KEY",
        "YANDEX_MAPS_API_KEY",
        "BRAVE_SEARCH_API_KEY",
    ):
        monkeypatch.delenv(key, raising=False)


def test_run_command_rejects_a_job_config_with_no_seeds_channels_or_provider_credentials(
    tmp_path,
):
    from lead_harvester import cli

    config_file = tmp_path / "job.yaml"
    config_file.write_text("categories: [FORMAL_EDUCATION]\n")

    result = cli.run_command(argparse.Namespace(config=str(config_file)))

    assert result == 2


def test_run_command_accepts_search_queries_alone(tmp_path):
    from lead_harvester import cli

    config_file = tmp_path / "job.yaml"
    config_file.write_text("search_queries: ['school in Karachi']\n")

    result = cli.run_command(argparse.Namespace(config=str(config_file)))

    # No BRAVE_SEARCH_API_KEY set -- _run_web_crawler logs and skips search
    # discovery, then finds no seeds and returns cleanly rather than
    # raising, so run_command still reports success.
    assert result == 0


def test_run_command_accepts_apple_maps_provider_with_credentials(tmp_path, monkeypatch):
    from lead_harvester import cli

    monkeypatch.setenv("APPLE_MAPS_TEAM_ID", "team1")
    monkeypatch.setenv("APPLE_MAPS_KEY_ID", "key1")
    monkeypatch.setenv("APPLE_MAPS_PRIVATE_KEY", "dummy-key")

    config_file = tmp_path / "job.yaml"
    config_file.write_text("places_provider: apple\ncities: {}\n")

    with patch(
        "lead_harvester.pipeline.LeadPipeline.run", new=AsyncMock(return_value=True)
    ) as run_mock:
        result = cli.run_command(argparse.Namespace(config=str(config_file)))

    run_mock.assert_awaited_once()
    assert result == 0


def test_run_command_rejects_apple_maps_provider_without_credentials(tmp_path):
    from lead_harvester import cli

    config_file = tmp_path / "job.yaml"
    config_file.write_text("places_provider: apple\ncities: {}\n")

    result = cli.run_command(argparse.Namespace(config=str(config_file)))

    assert result == 2


@pytest.mark.asyncio
async def test_linkedin_login_blocked_when_restricted_sources_disabled():
    # docs/ROADMAP.md Module 28: disabled by default -- must never attempt
    # the camoufox import or open a browser at all.
    from lead_harvester import cli

    args = argparse.Namespace(account="burner_01")

    result = await cli.linkedin_login(args)

    assert result == 1


@pytest.mark.asyncio
async def test_linkedin_run_blocked_when_restricted_sources_disabled(tmp_path, db_session):
    # docs/ROADMAP.md Module 28: disabled by default -- must never reach
    # LinkedInStealthCrawler at all, not just fail somewhere inside it.
    from lead_harvester import cli

    urls_file = tmp_path / "urls.txt"
    urls_file.write_text("https://linkedin.com/in/alice\n")

    args = argparse.Namespace(
        account="burner_01",
        urls_file=str(urls_file),
        proxy="",
        captcha_key="",
    )

    with patch(
        "lead_harvester.sources.linkedin_stealth.LinkedInStealthCrawler"
    ) as mock_crawler_cls:
        result = await cli.linkedin_run(args)

    assert result == 1
    mock_crawler_cls.assert_not_called()


@pytest.mark.asyncio
async def test_linkedin_run_constructs_crawler_without_unsupported_kwargs(
    tmp_path, db_session, _restricted_sources_enabled
):
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
async def test_linkedin_run_persists_partial_profiles_when_crawler_aborts(
    tmp_path, db_session, _restricted_sources_enabled
):
    # A CAPTCHA-triggered abort (or any other browser-level failure) after
    # earlier URLs already succeeded previously lost every profile
    # harvested so far -- crawler.run() raising meant this method never
    # reached its persistence block at all. run() attaches whatever it
    # collected before the exception to partial_profiles.
    from lead_harvester import cli

    urls_file = tmp_path / "urls.txt"
    urls_file.write_text("https://linkedin.com/in/alice\nhttps://linkedin.com/in/bob\n")

    args = argparse.Namespace(
        account="burner_01",
        urls_file=str(urls_file),
        proxy="",
        captcha_key="",
    )

    fake_profile = LinkedInProfile(profile_url="https://linkedin.com/in/alice", full_name="Alice")
    abort = RuntimeError("CaptchaTriggered:burner_01")
    abort.partial_profiles = [fake_profile]

    with (
        patch("lead_harvester.sources.linkedin_stealth.LinkedInStealthCrawler") as mock_crawler_cls,
        patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)),
    ):
        mock_crawler_cls.return_value.run = AsyncMock(side_effect=abort)
        result = await cli.linkedin_run(args)

    assert result == 1

    records = (
        (
            await db_session.execute(
                select(RawSourceRecord).where(RawSourceRecord.source_type == SourceType.LINKEDIN)
            )
        )
        .scalars()
        .all()
    )
    assert len(records) == 1
    assert records[0].source_id == "https://linkedin.com/in/alice"


@pytest.mark.asyncio
async def test_linkedin_run_isolates_a_db_level_failure_per_profile(
    tmp_path, db_session, _restricted_sources_enabled
):
    # RawSourceRecord.source_id is a VARCHAR(255) -- a genuine DB-level
    # error (StringDataRightTruncation), not a Python exception, if one
    # profile's URL exceeds that length. Without a per-row SAVEPOINT this
    # poisons the whole shared session, losing every other profile the
    # crawl harvested this run, not just the one bad row.
    from lead_harvester import cli

    urls_file = tmp_path / "urls.txt"
    urls_file.write_text("https://linkedin.com/in/alice\n")

    args = argparse.Namespace(
        account="burner_01",
        urls_file=str(urls_file),
        proxy="",
        captcha_key="",
    )

    too_long_url = "https://linkedin.com/in/" + "x" * 300
    profiles = [
        LinkedInProfile(profile_url="https://linkedin.com/in/alice", full_name="Alice"),
        LinkedInProfile(profile_url=too_long_url, full_name="Bad Row"),
        LinkedInProfile(profile_url="https://linkedin.com/in/bob", full_name="Bob"),
    ]

    with (
        patch("lead_harvester.sources.linkedin_stealth.LinkedInStealthCrawler") as mock_crawler_cls,
        patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)),
    ):
        mock_crawler_cls.return_value.run = AsyncMock(return_value=profiles)
        result = await cli.linkedin_run(args)

    assert result == 0

    records = (
        (
            await db_session.execute(
                select(RawSourceRecord).where(RawSourceRecord.source_type == SourceType.LINKEDIN)
            )
        )
        .scalars()
        .all()
    )
    assert {r.source_id for r in records} == {
        "https://linkedin.com/in/alice",
        "https://linkedin.com/in/bob",
    }


@pytest.mark.asyncio
async def test_issue_service_credential_prints_a_token_that_authenticates(db_session, capsys):
    from lead_harvester import cli
    from lead_harvester.models.auth import ServiceCredential
    from lead_harvester.services.auth_service import (
        authenticate_token,
        wait_for_pending_last_used_writes,
    )

    args = argparse.Namespace(name="cli-test-admin", role="admin", tenant_id="", ttl_days=0)

    with patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)):
        result = await cli.issue_service_credential(args)

    assert result == 0

    credential = (
        await db_session.execute(
            select(ServiceCredential).where(ServiceCredential.name == "cli-test-admin")
        )
    ).scalar_one()
    assert credential.role.value == "admin"
    assert credential.tenant_id == DEFAULT_TENANT_ID

    printed = capsys.readouterr().out
    raw_token = printed.rsplit(": ", 1)[1].strip()

    # authenticate_token() records last_used_at on its own independent
    # session (database.py's get_session(), bound to DATABASE_URL) --
    # redirect that to db_session the same way issue_service_credential
    # above was redirected.
    with patch(
        "lead_harvester.services.auth_service.get_session",
        new=lambda: _fake_get_session(db_session),
    ):
        authenticated = await authenticate_token(db_session, raw_token)
        await wait_for_pending_last_used_writes()
    assert authenticated is not None
    assert authenticated.id == credential.id


@pytest.mark.asyncio
async def test_issue_service_credential_rejects_invalid_role(db_session):
    from lead_harvester import cli

    args = argparse.Namespace(name="cli-test-bad-role", role="superuser", tenant_id="", ttl_days=0)

    result = await cli.issue_service_credential(args)

    assert result == 1


@pytest.mark.asyncio
async def test_issue_service_credential_rejects_invalid_tenant_id(db_session):
    from lead_harvester import cli

    args = argparse.Namespace(
        name="cli-test-bad-tenant", role="admin", tenant_id="not-a-uuid", ttl_days=0
    )

    result = await cli.issue_service_credential(args)

    assert result == 1


@pytest.mark.asyncio
async def test_issue_service_credential_rejects_a_non_default_tenant_id(db_session):
    # Tenant scoping only covers CanonicalInstitution/Branch/ContactPoint
    # and InstitutionService's reads so far -- a credential actually
    # authenticated as a non-default tenant would see every other
    # tenant's data through every unscoped route, so issuance for one
    # must be refused outright rather than silently look supported.
    from lead_harvester import cli
    from lead_harvester.models.tenancy import Tenant

    tenant = Tenant(name="Explicit Tenant Co", slug="explicit-tenant-co")
    db_session.add(tenant)
    await db_session.flush()

    args = argparse.Namespace(
        name="cli-test-explicit-tenant", role="admin", tenant_id=str(tenant.id), ttl_days=0
    )

    with patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)):
        result = await cli.issue_service_credential(args)

    assert result == 1


@pytest.mark.asyncio
async def test_issue_service_credential_accepts_the_default_tenant_id_explicitly(db_session):
    from lead_harvester import cli
    from lead_harvester.models.auth import ServiceCredential

    args = argparse.Namespace(
        name="cli-test-explicit-default-tenant",
        role="admin",
        tenant_id=str(DEFAULT_TENANT_ID),
        ttl_days=0,
    )

    with patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)):
        result = await cli.issue_service_credential(args)

    assert result == 0

    credential = (
        await db_session.execute(
            select(ServiceCredential).where(
                ServiceCredential.name == "cli-test-explicit-default-tenant"
            )
        )
    ).scalar_one()
    assert credential.tenant_id == DEFAULT_TENANT_ID


@pytest.mark.asyncio
async def test_issue_service_credential_sets_expires_at_from_ttl_days(db_session):
    import datetime as dt

    from lead_harvester import cli
    from lead_harvester.models.auth import ServiceCredential

    args = argparse.Namespace(name="cli-test-ttl", role="admin", tenant_id="", ttl_days=7)

    before = dt.datetime.now(dt.UTC)
    with patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)):
        result = await cli.issue_service_credential(args)
    after = dt.datetime.now(dt.UTC)

    assert result == 0

    credential = (
        await db_session.execute(
            select(ServiceCredential).where(ServiceCredential.name == "cli-test-ttl")
        )
    ).scalar_one()
    assert credential.expires_at is not None
    assert before + dt.timedelta(days=7) <= credential.expires_at <= after + dt.timedelta(days=7)


@pytest.mark.asyncio
async def test_issue_service_credential_rejects_a_negative_ttl(db_session):
    from lead_harvester import cli

    args = argparse.Namespace(name="cli-test-bad-ttl", role="admin", tenant_id="", ttl_days=-1)

    result = await cli.issue_service_credential(args)

    assert result == 1


@pytest.mark.asyncio
async def test_issue_service_credential_defaults_to_no_expiry(db_session):
    from lead_harvester import cli
    from lead_harvester.models.auth import ServiceCredential

    args = argparse.Namespace(name="cli-test-no-ttl", role="admin", tenant_id="", ttl_days=0)

    with patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)):
        result = await cli.issue_service_credential(args)

    assert result == 0

    credential = (
        await db_session.execute(
            select(ServiceCredential).where(ServiceCredential.name == "cli-test-no-ttl")
        )
    ).scalar_one()
    assert credential.expires_at is None


@pytest.mark.asyncio
async def test_revoke_service_credential_cmd_revokes_an_existing_credential(db_session):
    from lead_harvester import cli
    from lead_harvester.models.auth import ServiceRole
    from lead_harvester.services.auth_service import issue_service_credential

    await issue_service_credential(db_session, name="cli-test-revoke", role=ServiceRole.VIEWER)
    await db_session.commit()

    args = argparse.Namespace(name="cli-test-revoke")

    with patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)):
        result = await cli.revoke_service_credential_cmd(args)

    assert result == 0


@pytest.mark.asyncio
async def test_revoke_service_credential_cmd_errors_for_unknown_name(db_session):
    from lead_harvester import cli

    args = argparse.Namespace(name="cli-test-does-not-exist")

    with patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)):
        result = await cli.revoke_service_credential_cmd(args)

    assert result == 1


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
async def test_linkedin_farm_run_blocked_when_restricted_sources_disabled(tmp_path):
    # docs/ROADMAP.md Module 28: disabled by default -- must never reach
    # AccountFarm at all, not just fail somewhere inside it.
    from lead_harvester import cli

    urls_file = tmp_path / "urls.txt"
    urls_file.write_text("https://linkedin.com/in/alice\n")

    args = argparse.Namespace(
        accounts="burner_01",
        urls_file=str(urls_file),
        proxies_file="",
        captcha_key="",
        vertical="",
        target_city="",
        noise_urls_file="",
    )

    with patch("lead_harvester.sources.account_farm.AccountFarm") as mock_farm_cls:
        result = await cli._linkedin_farm_run(args)

    assert result == 1
    mock_farm_cls.assert_not_called()


@pytest.mark.asyncio
async def test_linkedin_farm_run_aborts_when_proxies_file_missing(
    tmp_path, _restricted_sources_enabled
):
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


@pytest.mark.asyncio
async def test_linkedin_farm_run_passes_vertical_and_noise_urls_through(
    tmp_path, _restricted_sources_enabled
):
    # --vertical/--target-city declare what this batch targets, enforcing
    # BreadthTracker's 30-day breadth ceiling before assignment, and
    # --noise-urls-file supplies the pool needs_noise_visit draws from --
    # both must actually reach AccountFarm.run(), not just be parsed and
    # discarded.
    from lead_harvester import cli

    urls_file = tmp_path / "urls.txt"
    urls_file.write_text("https://linkedin.com/in/alice\n")

    noise_urls_file = tmp_path / "noise.txt"
    noise_urls_file.write_text("https://linkedin.com/in/noise-a\nhttps://linkedin.com/in/noise-b\n")

    args = argparse.Namespace(
        accounts="burner_01",
        urls_file=str(urls_file),
        proxies_file="",
        captcha_key="",
        vertical="school_principals",
        target_city="karachi",
        noise_urls_file=str(noise_urls_file),
    )

    with patch("lead_harvester.sources.account_farm.AccountFarm") as mock_farm_cls:
        mock_farm_cls.return_value.run = AsyncMock(return_value=[])
        result = await cli._linkedin_farm_run(args)

    assert result == 0
    mock_farm_cls.return_value.run.assert_awaited_once_with(
        ["https://linkedin.com/in/alice"],
        vertical="school_principals",
        target_city="karachi",
        noise_urls=["https://linkedin.com/in/noise-a", "https://linkedin.com/in/noise-b"],
    )


@pytest.mark.asyncio
async def test_linkedin_farm_run_defaults_vertical_and_target_city_to_unknown(
    tmp_path, _restricted_sources_enabled
):
    from lead_harvester import cli

    urls_file = tmp_path / "urls.txt"
    urls_file.write_text("https://linkedin.com/in/alice\n")

    args = argparse.Namespace(
        accounts="burner_01",
        urls_file=str(urls_file),
        proxies_file="",
        captcha_key="",
        vertical="",
        target_city="",
        noise_urls_file="",
    )

    with patch("lead_harvester.sources.account_farm.AccountFarm") as mock_farm_cls:
        mock_farm_cls.return_value.run = AsyncMock(return_value=[])
        result = await cli._linkedin_farm_run(args)

    assert result == 0
    mock_farm_cls.return_value.run.assert_awaited_once_with(
        ["https://linkedin.com/in/alice"],
        vertical="unknown",
        target_city="unknown",
        noise_urls=None,
    )


@pytest.mark.asyncio
async def test_linkedin_farm_run_returns_failure_when_every_account_errors(
    tmp_path, _restricted_sources_enabled
):
    # AccountFarm.run() previously returned its list of AccountResult but
    # _linkedin_farm_run always returned 0 regardless -- a scheduler had no
    # way to tell a fully-failed harvest (every session missing, every
    # worker crashed or timed out) from a genuinely successful one.
    from lead_harvester import cli

    urls_file = tmp_path / "urls.txt"
    urls_file.write_text("https://linkedin.com/in/alice\n")

    args = argparse.Namespace(
        accounts="burner_01,burner_02",
        urls_file=str(urls_file),
        proxies_file="",
        captcha_key="",
        vertical="",
        target_city="",
        noise_urls_file="",
    )

    failed_results = [
        AccountResult(account_id="burner_01", profiles_scraped=0, errors=["No session saved"]),
        AccountResult(account_id="burner_02", profiles_scraped=0, errors=["Worker timed out"]),
    ]

    with patch("lead_harvester.sources.account_farm.AccountFarm") as mock_farm_cls:
        mock_farm_cls.return_value.run = AsyncMock(return_value=failed_results)
        result = await cli._linkedin_farm_run(args)

    assert result == 1


@pytest.mark.asyncio
async def test_linkedin_farm_run_succeeds_when_at_least_one_account_reports_no_errors(
    tmp_path, _restricted_sources_enabled
):
    from lead_harvester import cli

    urls_file = tmp_path / "urls.txt"
    urls_file.write_text("https://linkedin.com/in/alice\n")

    args = argparse.Namespace(
        accounts="burner_01,burner_02",
        urls_file=str(urls_file),
        proxies_file="",
        captcha_key="",
        vertical="",
        target_city="",
        noise_urls_file="",
    )

    mixed_results = [
        AccountResult(account_id="burner_01", profiles_scraped=3, errors=[]),
        AccountResult(account_id="burner_02", profiles_scraped=0, errors=["No session saved"]),
    ]

    with patch("lead_harvester.sources.account_farm.AccountFarm") as mock_farm_cls:
        mock_farm_cls.return_value.run = AsyncMock(return_value=mixed_results)
        result = await cli._linkedin_farm_run(args)

    assert result == 0


@pytest.mark.asyncio
async def test_linkedin_farm_run_succeeds_on_legitimate_no_op_skip(
    tmp_path, _restricted_sources_enabled
):
    # An empty results list means run() legitimately skipped the whole day
    # (outside working hours, or a weekend) -- not a failure.
    from lead_harvester import cli

    urls_file = tmp_path / "urls.txt"
    urls_file.write_text("https://linkedin.com/in/alice\n")

    args = argparse.Namespace(
        accounts="burner_01",
        urls_file=str(urls_file),
        proxies_file="",
        captcha_key="",
        vertical="",
        target_city="",
        noise_urls_file="",
    )

    with patch("lead_harvester.sources.account_farm.AccountFarm") as mock_farm_cls:
        mock_farm_cls.return_value.run = AsyncMock(return_value=[])
        result = await cli._linkedin_farm_run(args)

    assert result == 0


@pytest.mark.asyncio
async def test_linkedin_farm_run_rejects_proxies_file_missing_an_account(
    tmp_path, _restricted_sources_enabled
):
    # The file exists and covers burner_01, but says nothing about
    # burner_02 -- account_farm.py's dict.get("burner_02") would silently
    # return None and launch that one account unproxied from the host's
    # real IP, exactly what an explicit --proxies-file is meant to prevent.
    from lead_harvester import cli

    urls_file = tmp_path / "urls.txt"
    urls_file.write_text("https://linkedin.com/in/alice\n")

    proxies_file = tmp_path / "proxies.txt"
    proxies_file.write_text("burner_01=http://user:pass@proxy1:8080\n")

    args = argparse.Namespace(
        accounts="burner_01,burner_02",
        urls_file=str(urls_file),
        proxies_file=str(proxies_file),
        captcha_key="",
    )

    result = await cli._linkedin_farm_run(args)

    assert result == 1


@pytest.mark.asyncio
async def test_linkedin_farm_run_rejects_proxies_file_with_malformed_line(
    tmp_path, _restricted_sources_enabled
):
    # A line with no "=" (or a blank value after it) never lands in the
    # proxy map at all -- must be treated the same as a missing account,
    # not silently skipped.
    from lead_harvester import cli

    urls_file = tmp_path / "urls.txt"
    urls_file.write_text("https://linkedin.com/in/alice\n")

    proxies_file = tmp_path / "proxies.txt"
    proxies_file.write_text("burner_01=\nnot-a-valid-line\n")

    args = argparse.Namespace(
        accounts="burner_01",
        urls_file=str(urls_file),
        proxies_file=str(proxies_file),
        captcha_key="",
    )

    result = await cli._linkedin_farm_run(args)

    assert result == 1


@pytest.mark.asyncio
async def test_linkedin_send_returns_zero_when_automator_reports_success(tmp_path):
    from lead_harvester import cli

    args = argparse.Namespace(
        account="burner_01",
        smtp_host="",
        smtp_port="587",
        smtp_user="",
        from_name="",
        proxy="",
        dry_run=False,
    )

    with patch(
        "lead_harvester.outreach.automator.OutreachAutomator.run", new=AsyncMock(return_value=True)
    ):
        result = await cli.linkedin_send(args)

    assert result == 0


@pytest.mark.asyncio
async def test_linkedin_send_returns_one_when_automator_reports_policy_block(tmp_path):
    from lead_harvester import cli

    args = argparse.Namespace(
        account="burner_01",
        smtp_host="",
        smtp_port="587",
        smtp_user="",
        from_name="",
        proxy="",
        dry_run=False,
    )

    with patch(
        "lead_harvester.outreach.automator.OutreachAutomator.run",
        new=AsyncMock(return_value=False),
    ):
        result = await cli.linkedin_send(args)

    assert result == 1


@pytest.mark.asyncio
async def test_get_tenant_config_cmd_prints_the_registry_default(db_session, capsys):
    from lead_harvester import cli

    args = argparse.Namespace(tenant_id=str(DEFAULT_TENANT_ID), key="limit.export_max_rows")

    with patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)):
        result = await cli.get_tenant_config_cmd(args)

    assert result == 0
    assert "5000" in capsys.readouterr().out


@pytest.mark.asyncio
async def test_get_tenant_config_cmd_rejects_an_invalid_tenant_id():
    from lead_harvester import cli

    args = argparse.Namespace(tenant_id="not-a-uuid", key="limit.export_max_rows")

    result = await cli.get_tenant_config_cmd(args)

    assert result == 1


@pytest.mark.asyncio
async def test_get_tenant_config_cmd_rejects_an_unknown_key(db_session):
    from lead_harvester import cli

    args = argparse.Namespace(tenant_id=str(DEFAULT_TENANT_ID), key="not.a.real.key")

    with patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)):
        result = await cli.get_tenant_config_cmd(args)

    assert result == 1


@pytest.mark.asyncio
async def test_get_tenant_config_cmd_reports_a_clean_error_for_an_unknown_tenant(db_session):
    # A syntactically valid but nonexistent tenant must not silently print
    # the registry default and exit 0 as though that tenant existed.
    from lead_harvester import cli

    args = argparse.Namespace(tenant_id=str(uuid.uuid4()), key="limit.export_max_rows")

    with patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)):
        result = await cli.get_tenant_config_cmd(args)

    assert result == 1


@pytest.mark.asyncio
async def test_set_tenant_config_cmd_sets_a_bool_value(db_session, capsys):
    from lead_harvester import cli
    from lead_harvester.services.tenant_config_service import get_tenant_config

    args = argparse.Namespace(
        tenant_id=str(DEFAULT_TENANT_ID),
        key="feature.restricted_sources_enabled",
        value="true",
        set_by="test-operator",
    )

    with patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)):
        result = await cli.set_tenant_config_cmd(args)

    assert result == 0
    assert "version 1" in capsys.readouterr().out

    value = await get_tenant_config(
        db_session, DEFAULT_TENANT_ID, "feature.restricted_sources_enabled"
    )
    assert value is True


@pytest.mark.asyncio
async def test_set_tenant_config_cmd_sets_an_int_value(db_session):
    from lead_harvester import cli
    from lead_harvester.services.tenant_config_service import get_tenant_config

    args = argparse.Namespace(
        tenant_id=str(DEFAULT_TENANT_ID),
        key="limit.export_max_rows",
        value="42",
        set_by="test-operator",
    )

    with patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)):
        result = await cli.set_tenant_config_cmd(args)

    assert result == 0
    value = await get_tenant_config(db_session, DEFAULT_TENANT_ID, "limit.export_max_rows")
    assert value == 42


@pytest.mark.asyncio
async def test_set_tenant_config_cmd_rejects_an_unknown_key(db_session):
    from lead_harvester import cli

    args = argparse.Namespace(
        tenant_id=str(DEFAULT_TENANT_ID), key="not.a.real.key", value="x", set_by="test-operator"
    )

    result = await cli.set_tenant_config_cmd(args)

    assert result == 1


@pytest.mark.asyncio
async def test_set_tenant_config_cmd_rejects_a_malformed_bool_value(db_session):
    from lead_harvester import cli

    args = argparse.Namespace(
        tenant_id=str(DEFAULT_TENANT_ID),
        key="feature.restricted_sources_enabled",
        value="not-a-bool",
        set_by="test-operator",
    )

    result = await cli.set_tenant_config_cmd(args)

    assert result == 1


@pytest.mark.asyncio
async def test_set_tenant_config_cmd_rejects_an_invalid_tenant_id():
    from lead_harvester import cli

    args = argparse.Namespace(
        tenant_id="not-a-uuid",
        key="limit.export_max_rows",
        value="10",
        set_by="test-operator",
    )

    result = await cli.set_tenant_config_cmd(args)

    assert result == 1


@pytest.mark.asyncio
async def test_set_tenant_config_cmd_reports_a_clean_error_for_an_unknown_tenant(db_session):
    # A syntactically valid UUID that matches no Tenant row must raise a
    # controlled error, not an uncaught IntegrityError from the FK flush.
    from lead_harvester import cli

    args = argparse.Namespace(
        tenant_id=str(uuid.uuid4()),
        key="limit.export_max_rows",
        value="10",
        set_by="test-operator",
    )

    with patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)):
        result = await cli.set_tenant_config_cmd(args)

    assert result == 1


@pytest.fixture
def _vault_key(monkeypatch):
    from cryptography.fernet import Fernet

    from lead_harvester.config import settings

    monkeypatch.setattr(settings, "vault_encryption_key", Fernet.generate_key().decode())


@pytest.mark.asyncio
async def test_vault_store_credential_cmd_stores_and_prints_fingerprint_not_the_value(
    db_session, capsys, monkeypatch, _vault_key
):
    import io

    from lead_harvester import cli
    from lead_harvester.services.credential_vault_service import retrieve_plaintext_for_use
    from lead_harvester.vault_crypto import fingerprint_secret

    args = argparse.Namespace(
        tenant_id=str(DEFAULT_TENANT_ID),
        name="google_places_api_key",
        value_stdin=True,
        set_by="test-operator",
    )
    monkeypatch.setattr("sys.stdin", io.StringIO("the-real-secret-value\n"))

    with patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)):
        result = await cli.vault_store_credential_cmd(args)

    assert result == 0
    output = capsys.readouterr().out
    assert fingerprint_secret("the-real-secret-value") in output
    assert "the-real-secret-value" not in output

    value = await retrieve_plaintext_for_use(db_session, DEFAULT_TENANT_ID, "google_places_api_key")
    assert value == "the-real-secret-value"


@pytest.mark.asyncio
async def test_vault_store_credential_cmd_rejects_an_invalid_tenant_id(_vault_key):
    from lead_harvester import cli

    # Invalid --tenant-id is rejected before ever reading a value, so
    # this never touches stdin/getpass.
    args = argparse.Namespace(
        tenant_id="not-a-uuid", name="some-key", value_stdin=True, set_by="test-operator"
    )

    result = await cli.vault_store_credential_cmd(args)

    assert result == 1


@pytest.mark.asyncio
async def test_vault_store_credential_cmd_reports_a_clean_error_when_vault_is_unconfigured(
    db_session, monkeypatch
):
    import io

    from lead_harvester import cli

    args = argparse.Namespace(
        tenant_id=str(DEFAULT_TENANT_ID), name="some-key", value_stdin=True, set_by="test-operator"
    )
    monkeypatch.setattr("sys.stdin", io.StringIO("x\n"))

    with patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)):
        result = await cli.vault_store_credential_cmd(args)

    assert result == 1


@pytest.mark.asyncio
async def test_vault_store_credential_cmd_rejects_an_empty_value(
    db_session, monkeypatch, _vault_key
):
    import io

    from lead_harvester import cli

    args = argparse.Namespace(
        tenant_id=str(DEFAULT_TENANT_ID), name="some-key", value_stdin=True, set_by="test-operator"
    )
    monkeypatch.setattr("sys.stdin", io.StringIO("\n"))

    result = await cli.vault_store_credential_cmd(args)

    assert result == 1


@pytest.mark.asyncio
async def test_vault_show_credential_cmd_prints_fingerprint_not_the_value(
    db_session, capsys, _vault_key
):
    from lead_harvester import cli
    from lead_harvester.services.credential_vault_service import store_credential
    from lead_harvester.vault_crypto import fingerprint_secret

    await store_credential(
        db_session, DEFAULT_TENANT_ID, "show-me", "the-real-secret-value", created_by="op"
    )
    await db_session.commit()

    args = argparse.Namespace(tenant_id=str(DEFAULT_TENANT_ID), name="show-me")

    with patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)):
        result = await cli.vault_show_credential_cmd(args)

    assert result == 0
    output = capsys.readouterr().out
    assert fingerprint_secret("the-real-secret-value") in output
    assert "the-real-secret-value" not in output


@pytest.mark.asyncio
async def test_vault_show_credential_cmd_reports_a_clean_error_for_an_unknown_name(db_session):
    from lead_harvester import cli

    args = argparse.Namespace(tenant_id=str(DEFAULT_TENANT_ID), name="never-stored")

    with patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)):
        result = await cli.vault_show_credential_cmd(args)

    assert result == 1


@pytest.mark.asyncio
async def test_vault_revoke_credential_cmd_revokes_the_active_credential(db_session, _vault_key):
    from lead_harvester import cli
    from lead_harvester.services.credential_vault_service import (
        get_credential_fingerprint,
        store_credential,
    )

    await store_credential(db_session, DEFAULT_TENANT_ID, "revoke-me", "value", created_by="op")
    await db_session.commit()

    args = argparse.Namespace(tenant_id=str(DEFAULT_TENANT_ID), name="revoke-me")

    with patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)):
        result = await cli.vault_revoke_credential_cmd(args)

    assert result == 0
    assert await get_credential_fingerprint(db_session, DEFAULT_TENANT_ID, "revoke-me") is None


@pytest.mark.asyncio
async def test_vault_revoke_credential_cmd_reports_a_clean_error_for_an_unknown_name(db_session):
    from lead_harvester import cli

    args = argparse.Namespace(tenant_id=str(DEFAULT_TENANT_ID), name="never-stored")

    with patch("lead_harvester.database.get_session", new=lambda: _fake_get_session(db_session)):
        result = await cli.vault_revoke_credential_cmd(args)

    assert result == 1
