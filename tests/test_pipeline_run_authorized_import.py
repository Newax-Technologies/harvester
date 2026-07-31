import contextlib

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.config import Settings
from lead_harvester.models.canonical import Branch, CanonicalInstitution, ContactPoint
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

    success = await pipeline.run()
    assert success is True

    run = (
        await db_session.execute(
            select(SourceRun).where(SourceRun.source_type == SourceType.AUTHORIZED_IMPORT)
        )
    ).scalar_one()
    assert run.run_metadata["source_reference"] == "license-2026-education-directory"
    assert run.run_metadata["institutions_parsed"] == 2
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

    beacon = next(i for i in institutions if i.canonical_name == "Beacon House School")
    branch = (
        await db_session.execute(select(Branch).where(Branch.institution_id == beacon.id))
    ).scalar_one()
    assert branch.city == "Karachi"
    assert branch.country_code == "PK"

    contact = (
        await db_session.execute(
            select(ContactPoint).where(ContactPoint.institution_id == beacon.id)
        )
    ).scalar_one()
    assert contact.contact_type == "phone"
    assert contact.person_name == "Ali Khan"
    assert contact.role == "Principal"


@pytest.mark.asyncio
async def test_run_authorized_import_preserves_non_phone_email_contacts(
    tmp_path, db_session, monkeypatch
):
    csv_path = tmp_path / "leads.csv"
    csv_path.write_text(
        "institution_name,contact_type,contact_value,person_name,role\n"
        "Beacon House School,whatsapp,+923001234567,Ali Khan,Admissions Officer\n"
    )

    pipeline = LeadPipeline(
        _settings(
            {
                "authorized_import_file": str(csv_path),
                "authorized_import_source_reference": "license-2026",
            }
        )
    )
    monkeypatch.setattr(
        "lead_harvester.pipeline.get_session", lambda: _fake_get_session(db_session)
    )

    await pipeline.run()

    contact = (await db_session.execute(select(ContactPoint))).scalar_one()
    assert contact.contact_type == "whatsapp"
    assert contact.contact_value == "+923001234567"
    assert contact.person_name == "Ali Khan"
    assert contact.role == "Admissions Officer"


@pytest.mark.asyncio
async def test_run_authorized_import_groups_multi_contact_rows_into_one_institution(
    tmp_path, db_session, monkeypatch
):
    # Two rows for the same school (a phone contact and an email contact)
    # previously became two independent raw records with no shared
    # phone/domain/geo signal for the resolution pipeline to link them --
    # each silently became its own separate canonical institution.
    csv_path = tmp_path / "leads.csv"
    csv_path.write_text(
        "institution_name,website,contact_type,contact_value,person_name,role\n"
        "Beacon House School,https://beaconhouse.example.edu,phone,+923001234567,Ali Khan,Principal\n"
        "Beacon House School,https://beaconhouse.example.edu,email,"
        "admissions@beaconhouse.example.edu,,\n"
    )

    pipeline = LeadPipeline(
        _settings(
            {
                "authorized_import_file": str(csv_path),
                "authorized_import_source_reference": "license-2026",
            }
        )
    )
    monkeypatch.setattr(
        "lead_harvester.pipeline.get_session", lambda: _fake_get_session(db_session)
    )

    await pipeline.run()

    institutions = (await db_session.execute(select(CanonicalInstitution))).scalars().all()
    assert len(institutions) == 1

    contacts = (await db_session.execute(select(ContactPoint))).scalars().all()
    assert {c.contact_type for c in contacts} == {"phone", "email"}


@pytest.mark.asyncio
async def test_run_authorized_import_is_idempotent_on_rerun(tmp_path, db_session, monkeypatch):
    csv_path = tmp_path / "leads.csv"
    csv_path.write_text(
        "institution_name,website,contact_type,contact_value\n"
        "Beacon House School,https://beaconhouse.example.edu,phone,+923001234567\n"
    )

    pipeline = LeadPipeline(
        _settings(
            {
                "authorized_import_file": str(csv_path),
                "authorized_import_source_reference": "license-2026",
            }
        )
    )
    monkeypatch.setattr(
        "lead_harvester.pipeline.get_session", lambda: _fake_get_session(db_session)
    )

    await pipeline.run()
    await pipeline.run()

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

    institutions = (await db_session.execute(select(CanonicalInstitution))).scalars().all()
    assert len(institutions) == 1


@pytest.mark.asyncio
async def test_run_authorized_import_merges_new_contact_into_existing_institution(
    tmp_path, db_session, monkeypatch
):
    # source_id is derived only from institution_name + website (see
    # AuthorizedImportInstitution.source_id) -- it intentionally ignores
    # contacts, so a re-import that adds a second contact for an already-
    # resolved institution must not be silently discarded as an unchanged
    # rerun; the new contact must reach the existing CanonicalInstitution.
    csv_path = tmp_path / "leads.csv"
    csv_path.write_text(
        "institution_name,website,contact_type,contact_value\n"
        "Beacon House School,https://beaconhouse.example.edu,phone,+923001234567\n"
    )

    pipeline = LeadPipeline(
        _settings(
            {
                "authorized_import_file": str(csv_path),
                "authorized_import_source_reference": "license-2026",
            }
        )
    )
    monkeypatch.setattr(
        "lead_harvester.pipeline.get_session", lambda: _fake_get_session(db_session)
    )

    await pipeline.run()

    csv_path.write_text(
        "institution_name,website,contact_type,contact_value\n"
        "Beacon House School,https://beaconhouse.example.edu,phone,+923001234567\n"
        "Beacon House School,https://beaconhouse.example.edu,email,"
        "admissions@beaconhouse.example.edu\n"
    )
    await pipeline.run()

    institutions = (await db_session.execute(select(CanonicalInstitution))).scalars().all()
    assert len(institutions) == 1

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
    # A new, immutable RawSourceRecord captures the updated snapshot rather
    # than mutating the original -- raw_source_records is append-only.
    assert len(records) == 2

    contacts = (await db_session.execute(select(ContactPoint))).scalars().all()
    assert {c.contact_type for c in contacts} == {"phone", "email"}

    run_2 = (
        (
            await db_session.execute(
                select(SourceRun)
                .where(SourceRun.source_type == SourceType.AUTHORIZED_IMPORT)
                .order_by(SourceRun.started_at.desc())
            )
        )
        .scalars()
        .first()
    )
    assert run_2.run_metadata["institutions_updated"] == 1


@pytest.mark.asyncio
async def test_run_authorized_import_enriches_existing_contact_person_name_and_role(
    tmp_path, db_session, monkeypatch
):
    # _authorized_import_has_new_evidence previously compared contacts only
    # by (contact_type, contact_value) -- a later CSV version filling in
    # person_name/role for an already-declared phone/email compared equal
    # to the existing set, so the whole institution was skipped as
    # unchanged and the new decision-maker metadata never reached
    # ContactPoint.
    csv_path = tmp_path / "leads.csv"
    csv_path.write_text(
        "institution_name,website,contact_type,contact_value\n"
        "Beacon House School,https://beaconhouse.example.edu,phone,+923001234567\n"
    )

    pipeline = LeadPipeline(
        _settings(
            {
                "authorized_import_file": str(csv_path),
                "authorized_import_source_reference": "license-2026",
            }
        )
    )
    monkeypatch.setattr(
        "lead_harvester.pipeline.get_session", lambda: _fake_get_session(db_session)
    )

    await pipeline.run()

    contact = (await db_session.execute(select(ContactPoint))).scalar_one()
    assert contact.person_name is None

    csv_path.write_text(
        "institution_name,website,contact_type,contact_value,person_name,role\n"
        "Beacon House School,https://beaconhouse.example.edu,phone,+923001234567,"
        "Ali Khan,Principal\n"
    )
    await pipeline.run()

    institutions = (await db_session.execute(select(CanonicalInstitution))).scalars().all()
    assert len(institutions) == 1

    contact = (await db_session.execute(select(ContactPoint))).scalar_one()
    assert contact.person_name == "Ali Khan"
    assert contact.role == "Principal"


@pytest.mark.asyncio
async def test_run_authorized_import_requires_source_reference(tmp_path, capsys):
    csv_path = tmp_path / "leads.csv"
    csv_path.write_text("institution_name,contact_value\nSchool A,+923001234567\n")

    pipeline = LeadPipeline(_settings({"authorized_import_file": str(csv_path)}))

    success = await pipeline.run()

    assert success is False
    assert "source_reference is required" in capsys.readouterr().out


@pytest.mark.asyncio
async def test_run_authorized_import_reports_failure_for_malformed_csv(tmp_path, capsys):
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

    success = await pipeline.run()

    assert success is False
    assert "malformed" in capsys.readouterr().out
