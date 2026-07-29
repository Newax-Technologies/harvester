from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from sqlalchemy import select

from lead_harvester.config import Settings
from lead_harvester.models.canonical import Branch, CanonicalInstitution
from lead_harvester.models.source import RunStatus, SourceRun, SourceType
from lead_harvester.pipeline import LeadPipeline


def _place(*, place_id: str, name: str, phone: str, lat: float, lng: float) -> dict:
    return {
        "id": place_id,
        "displayName": {"text": name},
        "formattedAddress": "1 Test Street",
        "websiteUri": f"https://{place_id}.example.edu",
        "primaryType": "school",
        "nationalPhoneNumber": phone,
        "location": {"latitude": lat, "longitude": lng},
    }


@pytest.fixture
def pipeline():
    return LeadPipeline(Settings(google_places_api_key="dummy-test-key"))


@pytest_asyncio.fixture
async def source_run(db_session):
    run = SourceRun(source_type=SourceType.GOOGLE_PLACES, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(run)
    await db_session.flush()
    return run


@pytest.mark.asyncio
async def test_process_place_creates_canonical_institution(db_session, pipeline, source_run):
    place = _place(
        place_id="gp-1", name="Sunrise Academy", phone="+923001231234", lat=24.86, lng=67.00
    )

    await pipeline.process_place(db_session, source_run, place)

    result = await db_session.execute(
        select(CanonicalInstitution).where(CanonicalInstitution.canonical_name == "sunrise academy")
    )
    institution = result.scalar_one()

    branches = (
        (await db_session.execute(select(Branch).where(Branch.institution_id == institution.id)))
        .scalars()
        .all()
    )
    assert len(branches) == 1


@pytest.mark.asyncio
async def test_process_place_merges_matching_places_into_one_institution(
    db_session, pipeline, source_run
):
    place_a = _place(
        place_id="gp-a", name="Twin Gate School", phone="+923005551111", lat=31.5, lng=74.3
    )
    place_b = _place(
        place_id="gp-b", name="Twin Gate School", phone="+923005552222", lat=31.5, lng=74.3
    )

    await pipeline.process_place(db_session, source_run, place_a)
    await pipeline.process_place(db_session, source_run, place_b)

    result = await db_session.execute(
        select(CanonicalInstitution).where(
            CanonicalInstitution.canonical_name == "twin gate school"
        )
    )
    institutions = result.scalars().all()
    assert len(institutions) == 1

    branches = (
        (
            await db_session.execute(
                select(Branch).where(Branch.institution_id == institutions[0].id)
            )
        )
        .scalars()
        .all()
    )
    assert len(branches) == 1


@pytest.mark.asyncio
async def test_resolution_failure_is_logged_not_raised(db_session, source_run):
    place = _place(
        place_id="gp-err", name="Failing School", phone="+923009990000", lat=1.0, lng=1.0
    )
    pipeline = LeadPipeline(Settings(google_places_api_key="dummy-test-key"))

    with patch(
        "lead_harvester.pipeline.resolve_incoming_record",
        new=AsyncMock(side_effect=RuntimeError("boom")),
    ):
        await pipeline.process_place(db_session, source_run, place)  # must not raise

    assert len(source_run.run_metadata["unresolved_records"]) == 1
    assert "boom" in source_run.run_metadata["unresolved_records"][0]["error"]
