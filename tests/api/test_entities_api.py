import uuid

import pytest

from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.signal import Signal, SignalType
from lead_harvester.services.person_candidate_service import resolve_person_candidate


@pytest.mark.asyncio
async def test_list_person_candidates_route(client_a, db_session):
    institution = CanonicalInstitution(canonical_name="Entities API School")
    db_session.add(institution)
    await db_session.flush()
    await resolve_person_candidate(db_session, institution.id, "Ali Khan")
    await db_session.commit()

    response = await client_a.get("/api/v1/entities/person-candidates")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["display_name"] == "Ali Khan"
    assert body[0]["institution_id"] == str(institution.id)


@pytest.mark.asyncio
async def test_list_person_candidates_route_filters_by_institution(client_a, db_session):
    institution_a = CanonicalInstitution(canonical_name="School A")
    institution_b = CanonicalInstitution(canonical_name="School B")
    db_session.add_all([institution_a, institution_b])
    await db_session.flush()
    await resolve_person_candidate(db_session, institution_a.id, "Ali Khan")
    await resolve_person_candidate(db_session, institution_b.id, "Jane Doe")
    await db_session.commit()

    response = await client_a.get(
        "/api/v1/entities/person-candidates", params={"institution_id": str(institution_a.id)}
    )

    body = response.json()
    assert len(body) == 1
    assert body[0]["display_name"] == "Ali Khan"


@pytest.mark.asyncio
async def test_list_signals_route(client_a, db_session):
    institution = CanonicalInstitution(canonical_name="Signals API School")
    db_session.add(institution)
    await db_session.flush()
    db_session.add(
        Signal(
            institution_id=institution.id,
            signal_type=SignalType.PAIN_POINT,
            signal_text="No CRM in place",
            source_url="https://linkedin.com/in/example",
            confidence_score=0.85,
        )
    )
    await db_session.commit()

    response = await client_a.get("/api/v1/entities/signals")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["signal_type"] == "pain_point"
    assert body[0]["signal_text"] == "No CRM in place"


@pytest.mark.asyncio
async def test_list_signals_route_filters_by_type(client_a, db_session):
    institution = CanonicalInstitution(canonical_name="Signals Filter School")
    db_session.add(institution)
    await db_session.flush()
    db_session.add_all(
        [
            Signal(
                institution_id=institution.id,
                signal_type=SignalType.PAIN_POINT,
                signal_text="No CRM in place",
            ),
            Signal(
                institution_id=institution.id,
                signal_type=SignalType.BUYING_SIGNAL,
                signal_text="Recently hired sales team",
            ),
        ]
    )
    await db_session.commit()

    response = await client_a.get(
        "/api/v1/entities/signals", params={"signal_type": "buying_signal"}
    )

    body = response.json()
    assert len(body) == 1
    assert body[0]["signal_text"] == "Recently hired sales team"


@pytest.mark.asyncio
async def test_list_signals_route_404s_are_not_expected_for_unknown_institution(client_a):
    # An unknown institution_id filter is a valid, empty-result query --
    # not an error -- there's nothing to 404 on for a list endpoint.
    response = await client_a.get(
        "/api/v1/entities/signals", params={"institution_id": str(uuid.uuid4())}
    )
    assert response.status_code == 200
    assert response.json() == []
