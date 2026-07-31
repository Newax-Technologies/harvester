import csv
import io
import json

import pytest

from lead_harvester.models.canonical import (
    Branch,
    CanonicalInstitution,
    ContactPoint,
    OperatingStatus,
)


async def _seed_institution(db_session, *, name: str) -> CanonicalInstitution:
    institution = CanonicalInstitution(
        canonical_name=name, status=OperatingStatus.OPERATIONAL, confidence_score=50.0
    )
    db_session.add(institution)
    await db_session.flush()
    db_session.add(
        Branch(
            institution_id=institution.id,
            branch_name="Main",
            city="Karachi",
            country_code="PK",
            provider_ids={},
        )
    )
    db_session.add(
        ContactPoint(
            institution_id=institution.id,
            contact_type="email",
            contact_value="lead@school.edu",
            person_name="Admissions Office",
            is_publicly_listed=True,
        )
    )
    await db_session.flush()
    return institution


@pytest.mark.asyncio
async def test_export_leads_route_defaults_to_csv(client_a, db_session):
    institution = await _seed_institution(db_session, name="CSV Export School")
    await db_session.commit()

    response = await client_a.get("/api/v1/exports/leads")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    rows = list(csv.DictReader(io.StringIO(response.text)))
    assert len(rows) == 1
    assert rows[0]["institution_id"] == str(institution.id)
    assert rows[0]["primary_city"] == "Karachi"


@pytest.mark.asyncio
async def test_export_leads_route_supports_json(client_a, db_session):
    institution = await _seed_institution(db_session, name="JSON Export School")
    await db_session.commit()

    response = await client_a.get("/api/v1/exports/leads", params={"format": "json"})

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    body = json.loads(response.text)
    assert len(body) == 1
    assert body[0]["institution_id"] == str(institution.id)
    assert body[0]["contact_value"] == "lead@school.edu"


@pytest.mark.asyncio
async def test_export_leads_route_respects_status_filter(client_a, db_session):
    await _seed_institution(db_session, name="Operational Export School")
    closed = CanonicalInstitution(
        canonical_name="Closed Export School", status=OperatingStatus.CLOSED_PERMANENTLY
    )
    db_session.add(closed)
    await db_session.flush()
    db_session.add(
        ContactPoint(
            institution_id=closed.id, contact_type="email", contact_value="closed@school.edu"
        )
    )
    await db_session.commit()

    response = await client_a.get(
        "/api/v1/exports/leads", params={"status": "closed_permanently", "format": "json"}
    )

    body = json.loads(response.text)
    assert len(body) == 1
    assert body[0]["institution_id"] == str(closed.id)
