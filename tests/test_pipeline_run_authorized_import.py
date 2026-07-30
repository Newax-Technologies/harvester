import contextlib

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.config import Settings
from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.source import RawSourceRecord, SourceRun, SourceType
from lead_harvester.pipeline import LeadPipeline

# _run_authorized_import opens its own session via database.get_session()
# (bound to settings.database_url, a real database CI never provisions) --
# same reasoning as tests/test_pipeline_run_resync.py. Patch get_session
# within the pipeline module to yield the isolated db_session fixture
# instead.


@contextlib.asynccontextmanager
async def _fake_get_session(session: AsyncSession):
    yield session


def _settings(job_config: dict) -> Settings:
    return Settings(google_places_api_key="dummy-test-key", job_config=job_config)


@pytest.mark.asyncio
async def test_run_authorized_import_creates_source_run_and_records(
    tmp_path, db_session, monkeypatch
):
    csv_path = tmp_path / "leads.csv"
    csv_path.write_text(
        "institution_name,institution_type,website,address,city,country,country_code,"
        "contact_type,contact_value,person_name,role,notes\n"
        "Beacon House School,school,https://beaconhouse.example.edu,"
        "Plot 12 Block B,Karachi,Pakistan,PK,phone,+923001234567,Ali Khan,Principal,Referral\n"
        "Riverside Academy,,,,,,,email,admissions@riverside.example.edu,,,\n"
        ",,,,,,,phone,+923009999999,,,\n"  # missing institution_name -- must be skipped, not crash
    )

    pipeline = LeadPipeline(
        _settings(
            {
                "authorized_import_file": str(csv_path),
                "authorized_import_source_reference": "license-2026-education-directory",
            }
        )
    )

    monkeypatch.setattr(
        "lead_harvester.pipeline.get_session", lambda: _fake_get_session(db_session)
    )

    await pipeline.run()

    run = (
        await db_session.execute(
            select(SourceRun).where(SourceRun.source_type == SourceType.AUTHORIZED_IMPORT)
        )
    ).scalar_one()
    assert run.run_metadata["source_reference"] == "license-2026-education-directory"
    assert run.run_metadata["rows_parsed"] == 2
    assert run.run_metadata["rows_skipped"] == 1

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
    assert len(records) == 2
    assert {r.normalized_name for r in records} == {"beacon house school", "riverside academy"}

    institutions = (await db_session.execute(select(CanonicalInstitution))).scalars().all()
    assert {i.canonical_name for i in institutions} == {"Beacon House School", "Riverside Academy"}


@pytest.mark.asyncio
async def test_run_authorized_import_requires_source_reference(tmp_path, capsys):
    csv_path = tmp_path / "leads.csv"
    csv_path.write_text("institution_name,contact_value\nSchool A,+923001234567\n")

    pipeline = LeadPipeline(_settings({"authorized_import_file": str(csv_path)}))

    await pipeline.run()

    assert "source_reference is required" in capsys.readouterr().out


@pytest.mark.asyncio
async def test_run_authorized_import_logs_missing_column_without_raising(tmp_path, capsys):
    csv_path = tmp_path / "leads.csv"
    csv_path.write_text("institution_name\nSchool A\n")  # missing contact_value column entirely

    pipeline = LeadPipeline(
        _settings(
            {
                "authorized_import_file": str(csv_path),
                "authorized_import_source_reference": "license-2026",
            }
        )
    )

    await pipeline.run()

    assert "malformed" in capsys.readouterr().out
