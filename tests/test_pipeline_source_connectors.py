import contextlib
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.config import Settings
from lead_harvester.models.canonical import Branch, CanonicalInstitution
from lead_harvester.models.source import RawSourceRecord, RunStatus, SourceRun, SourceType
from lead_harvester.pipeline import LeadPipeline
from lead_harvester.sources.search import SearchResult


@pytest.fixture
def pipeline():
    return LeadPipeline(Settings())


@pytest_asyncio.fixture
async def yandex_run(db_session):
    run = SourceRun(source_type=SourceType.YANDEX, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(run)
    await db_session.flush()
    return run


@pytest_asyncio.fixture
async def apple_run(db_session):
    run = SourceRun(source_type=SourceType.APPLE_MAPS, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(run)
    await db_session.flush()
    return run


@pytest_asyncio.fixture
async def telegram_run(db_session):
    run = SourceRun(source_type=SourceType.TELEGRAM, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(run)
    await db_session.flush()
    return run


def _yandex_feature(*, company_id: str, name: str, phone: str, lat: float, lng: float) -> dict:
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lng, lat]},
        "properties": {
            "name": name,
            "description": "Some Street, Karachi",
            "CompanyMetaData": {
                "id": company_id,
                "name": name,
                "address": "Some Street, Karachi",
                "Phones": [{"type": "phone", "formatted": phone}],
                "url": f"https://{company_id}.example.edu",
                "Categories": [{"name": "School"}],
            },
        },
    }


@pytest.mark.asyncio
async def test_process_yandex_place_creates_canonical_institution(db_session, pipeline, yandex_run):
    feature = _yandex_feature(
        company_id="yx-1", name="Riverside Academy", phone="+923001231234", lat=24.86, lng=67.00
    )

    await pipeline.process_yandex_place(db_session, yandex_run, feature)

    result = await db_session.execute(
        select(CanonicalInstitution).where(
            CanonicalInstitution.canonical_name == "Riverside Academy"
        )
    )
    institution = result.scalar_one()
    branches = (
        (await db_session.execute(select(Branch).where(Branch.institution_id == institution.id)))
        .scalars()
        .all()
    )
    assert len(branches) == 1


@pytest.mark.asyncio
async def test_process_yandex_place_skips_features_with_no_company_id(
    db_session, pipeline, yandex_run
):
    feature = {"type": "Feature", "geometry": {}, "properties": {"name": "No ID School"}}

    await pipeline.process_yandex_place(db_session, yandex_run, feature)

    result = await db_session.execute(
        select(CanonicalInstitution).where(CanonicalInstitution.canonical_name == "No ID School")
    )
    assert result.scalar_one_or_none() is None


def _apple_result(*, name: str, lat: float, lng: float) -> dict:
    return {
        "name": name,
        "formattedAddressLines": ["1 Test Street", "Karachi, Pakistan"],
        "coordinate": {"latitude": lat, "longitude": lng},
    }


@pytest.mark.asyncio
async def test_process_apple_place_creates_canonical_institution(db_session, pipeline, apple_run):
    result = _apple_result(name="Sunrise Academy", lat=24.86, lng=67.00)

    await pipeline.process_apple_place(db_session, apple_run, result)

    institution = (
        await db_session.execute(
            select(CanonicalInstitution).where(
                CanonicalInstitution.canonical_name == "Sunrise Academy"
            )
        )
    ).scalar_one()
    branches = (
        (await db_session.execute(select(Branch).where(Branch.institution_id == institution.id)))
        .scalars()
        .all()
    )
    assert len(branches) == 1
    assert branches[0].address == "1 Test Street, Karachi, Pakistan"


@pytest.mark.asyncio
async def test_process_apple_place_source_id_is_stable_for_the_same_name_and_address(
    db_session, pipeline, apple_run
):
    result_a = _apple_result(name="Twin Gate School", lat=31.5, lng=74.3)
    result_b = _apple_result(name="Twin Gate School", lat=31.5, lng=74.3)

    await pipeline.process_apple_place(db_session, apple_run, result_a)
    await pipeline.process_apple_place(db_session, apple_run, result_b)

    records = (
        (
            await db_session.execute(
                select(RawSourceRecord).where(RawSourceRecord.source_type == SourceType.APPLE_MAPS)
            )
        )
        .scalars()
        .all()
    )
    assert len(records) == 2
    assert records[0].source_id == records[1].source_id


@pytest.mark.asyncio
async def test_process_apple_place_skips_results_with_no_name(db_session, pipeline, apple_run):
    result = {"formattedAddressLines": ["1 Test Street"], "coordinate": {}}

    await pipeline.process_apple_place(db_session, apple_run, result)

    count = (await db_session.execute(select(CanonicalInstitution))).scalars().all()
    assert count == []


def _telegram_payload(*, channel: str, name: str, emails: list[str], phones: list[str]) -> dict:
    return {
        "channel": channel,
        "preview_url": f"https://t.me/s/{channel}",
        "name": name,
        "description": "",
        "all_emails": emails,
        "all_phones": phones,
    }


@pytest.mark.asyncio
async def test_process_telegram_channel_creates_canonical_institution(
    db_session, pipeline, telegram_run
):
    payload = _telegram_payload(
        channel="beaconhouseofficial",
        name="Beacon House School",
        emails=["admissions@beaconhouse.example.edu"],
        phones=["+923001234567"],
    )

    await pipeline.process_telegram_channel(db_session, telegram_run, payload)

    institution = (
        await db_session.execute(
            select(CanonicalInstitution).where(
                CanonicalInstitution.canonical_name == "Beacon House School"
            )
        )
    ).scalar_one()
    assert institution is not None


@pytest.mark.asyncio
async def test_process_telegram_channel_skips_payloads_with_no_name(
    db_session, pipeline, telegram_run
):
    payload = _telegram_payload(channel="emptychannel", name="", emails=[], phones=[])

    await pipeline.process_telegram_channel(db_session, telegram_run, payload)

    result = (await db_session.execute(select(CanonicalInstitution))).scalars().all()
    assert result == []


@pytest.mark.asyncio
async def test_run_dispatches_to_apple_maps_when_places_provider_is_apple():
    pipeline = LeadPipeline(Settings(job_config={"places_provider": "apple"}))
    with (
        patch.object(pipeline, "_run_apple_maps", new=AsyncMock()) as apple_mock,
        patch.object(pipeline, "_run_google_places", new=AsyncMock()) as google_mock,
    ):
        await pipeline.run()
    apple_mock.assert_awaited_once()
    google_mock.assert_not_awaited()


@pytest.mark.asyncio
async def test_run_dispatches_to_yandex_maps_when_places_provider_is_yandex():
    pipeline = LeadPipeline(Settings(job_config={"places_provider": "yandex"}))
    with (
        patch.object(pipeline, "_run_yandex_maps", new=AsyncMock()) as yandex_mock,
        patch.object(pipeline, "_run_google_places", new=AsyncMock()) as google_mock,
    ):
        await pipeline.run()
    yandex_mock.assert_awaited_once()
    google_mock.assert_not_awaited()


@pytest.mark.asyncio
async def test_run_dispatches_to_telegram_when_telegram_channels_configured():
    pipeline = LeadPipeline(Settings(job_config={"telegram_channels": ["beaconhouseofficial"]}))
    with (
        patch.object(pipeline, "_run_telegram", new=AsyncMock()) as telegram_mock,
        patch.object(pipeline, "_run_google_places", new=AsyncMock()) as google_mock,
    ):
        await pipeline.run()
    telegram_mock.assert_awaited_once()
    google_mock.assert_not_awaited()


@pytest.mark.asyncio
async def test_run_still_defaults_to_google_places_when_no_provider_configured():
    pipeline = LeadPipeline(Settings())
    with patch.object(pipeline, "_run_google_places", new=AsyncMock()) as google_mock:
        await pipeline.run()
    google_mock.assert_awaited_once()


@contextlib.asynccontextmanager
async def _fake_get_session(session: AsyncSession):
    yield session


@pytest.mark.asyncio
async def test_run_dispatches_to_web_crawler_when_only_search_queries_configured():
    pipeline = LeadPipeline(Settings(job_config={"search_queries": ["school in Karachi"]}))
    with (
        patch.object(pipeline, "_run_web_crawler", new=AsyncMock()) as web_mock,
        patch.object(pipeline, "_run_google_places", new=AsyncMock()) as google_mock,
    ):
        await pipeline.run()
    web_mock.assert_awaited_once()
    google_mock.assert_not_awaited()


@pytest.mark.asyncio
async def test_search_queries_discover_additional_seeds_for_the_web_crawler(db_session):
    pipeline = LeadPipeline(
        Settings(
            job_config={"search_queries": ["school in Karachi"]},
            brave_search_api_key="test-key",
        )
    )

    search_results = [
        SearchResult(title="Beacon House School", url="https://beaconhouse.example.edu"),
    ]
    crawl_mock = AsyncMock(return_value=[])

    with (
        patch(
            "lead_harvester.pipeline.get_session",
            new=lambda: _fake_get_session(db_session),
        ),
        patch(
            "lead_harvester.sources.search.BraveSearchSource.search",
            new=AsyncMock(return_value=search_results),
        ),
        patch("lead_harvester.sources.web.WebCrawler.crawl", new=crawl_mock),
    ):
        await pipeline._run_web_crawler()

    crawl_mock.assert_awaited_once_with(["https://beaconhouse.example.edu"])


@pytest.mark.asyncio
async def test_search_queries_without_api_key_do_not_discover_seeds():
    pipeline = LeadPipeline(Settings(job_config={"search_queries": ["school in Karachi"]}))

    with patch(
        "lead_harvester.sources.search.BraveSearchSource.search", new=AsyncMock()
    ) as search_mock:
        await pipeline._run_web_crawler()

    search_mock.assert_not_awaited()
