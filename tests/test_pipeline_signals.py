import pytest
import pytest_asyncio
from sqlalchemy import select

from lead_harvester.config import Settings
from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.signal import Signal, SignalType
from lead_harvester.models.source import RawSourceRecord, RunStatus, SourceRun, SourceType
from lead_harvester.pipeline import LeadPipeline
from lead_harvester.resolution.normalize import normalize_name


@pytest_asyncio.fixture
async def source_run(db_session):
    run = SourceRun(source_type=SourceType.WEBSITE, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(run)
    await db_session.flush()
    return run


@pytest.fixture
def pipeline():
    return LeadPipeline(Settings())


def _website_record(
    run, *, organization: str, website: str, detected_signals: list[dict]
) -> RawSourceRecord:
    return RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.WEBSITE,
        source_id=website,
        raw_payload={
            "source": "website",
            "source_url": website,
            "organization": organization,
            "raw": {"detected_signals": detected_signals},
        },
        normalized_name=normalize_name(organization),
        normalized_domain=website.replace("https://", "").replace("http://", ""),
    )


@pytest.mark.asyncio
async def test_resolving_a_website_record_materializes_detected_signal_rows(
    db_session, source_run, pipeline
):
    record = _website_record(
        source_run,
        organization="Beacon House School",
        website="https://beaconhouse.example.edu",
        detected_signals=[
            {
                "signal_type": "pain_point",
                "text": "Uses WhatsApp for communication with no online booking/portal.",
            },
            {
                "signal_type": "buying_signal",
                "text": "Actively hiring -- may indicate growth/budget.",
            },
        ],
    )
    db_session.add(record)
    await db_session.flush()

    await pipeline._resolve_or_log(db_session, source_run, record)

    institution = (
        await db_session.execute(
            select(CanonicalInstitution).where(
                CanonicalInstitution.canonical_name == "Beacon House School"
            )
        )
    ).scalar_one()

    signals = (
        (await db_session.execute(select(Signal).where(Signal.institution_id == institution.id)))
        .scalars()
        .all()
    )
    assert len(signals) == 2
    assert {s.signal_type for s in signals} == {SignalType.PAIN_POINT, SignalType.BUYING_SIGNAL}
    assert all(s.source_url == "https://beaconhouse.example.edu" for s in signals)
    assert all(s.confidence_score == 0.6 for s in signals)


@pytest.mark.asyncio
async def test_no_detected_signals_creates_no_signal_rows(db_session, source_run, pipeline):
    record = _website_record(
        source_run,
        organization="Riverside Academy",
        website="https://riverside.example.edu",
        detected_signals=[],
    )
    db_session.add(record)
    await db_session.flush()

    await pipeline._resolve_or_log(db_session, source_run, record)

    institution = (
        await db_session.execute(
            select(CanonicalInstitution).where(
                CanonicalInstitution.canonical_name == "Riverside Academy"
            )
        )
    ).scalar_one()

    signals = (
        (await db_session.execute(select(Signal).where(Signal.institution_id == institution.id)))
        .scalars()
        .all()
    )
    assert signals == []


@pytest.mark.asyncio
async def test_non_website_source_never_materializes_signals_even_if_raw_key_present(
    db_session, source_run, pipeline
):
    # Only the web crawler's Lead dataclass ever populates raw_payload["raw"],
    # but this proves _persist_detected_signals is genuinely gated on
    # SourceType.WEBSITE, not just on key presence.
    record = RawSourceRecord(
        source_run_id=source_run.id,
        source_type=SourceType.GOOGLE_PLACES,
        source_id="gp-signal-test",
        raw_payload={
            "id": "gp-signal-test",
            "displayName": {"text": "Sunrise Academy"},
            "raw": {
                "detected_signals": [
                    {"signal_type": "pain_point", "text": "Should not be persisted."}
                ]
            },
        },
        normalized_name=normalize_name("Sunrise Academy"),
    )
    db_session.add(record)
    await db_session.flush()

    await pipeline._resolve_or_log(db_session, source_run, record)

    institution = (
        await db_session.execute(
            select(CanonicalInstitution).where(
                CanonicalInstitution.canonical_name == "Sunrise Academy"
            )
        )
    ).scalar_one()

    signals = (
        (await db_session.execute(select(Signal).where(Signal.institution_id == institution.id)))
        .scalars()
        .all()
    )
    # GOOGLE_PLACES records legitimately carry no "raw" key in production,
    # but this record was crafted with one to prove the gate holds anyway --
    # it does not persist a Signal even though a detected_signals list is
    # present in raw_payload.
    assert signals == []
