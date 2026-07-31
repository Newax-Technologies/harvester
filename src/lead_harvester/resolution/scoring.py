from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from geoalchemy2.functions import ST_Distance

from lead_harvester.models.source import RawSourceRecord
from lead_harvester.models.canonical import CanonicalInstitution, Branch
from lead_harvester.models.resolution import ResolutionCandidate, MatchAssessment, MatchDecision


def _decide(name_similarity: float, distance_meters: float | None, phone_match: bool, domain_match: bool) -> tuple[float, MatchDecision]:
    """Shared scoring matrix / decision logic for both raw-record and canonical-institution targets."""
    decision = MatchDecision.REJECT
    total_score = 0.0

    if name_similarity > 0.8:
        total_score += 40
    elif name_similarity > 0.5:
        total_score += 20

    if distance_meters is not None and distance_meters < 50:
        total_score += 40
    elif distance_meters is not None and distance_meters < 200:
        total_score += 20

    if phone_match:
        total_score += 20
    if domain_match:
        total_score += 20

    if name_similarity > 0.8 and distance_meters is not None and distance_meters < 100:
        # Same name, same location -> Definitely the same entity (MERGE)
        decision = MatchDecision.MERGE
    elif phone_match or domain_match:
        # Shared contact details, but potentially different physical locations/names.
        # This prevents merging a franchise network into a single school.
        decision = MatchDecision.LINK_ONLY
    elif total_score > 60:
        # High overall confidence but lacking definitive proof
        decision = MatchDecision.PENDING

    return total_score, decision


async def score_candidate(session: AsyncSession, candidate: ResolutionCandidate) -> MatchAssessment:
    """
    Evaluates a candidate pairing and returns a MatchAssessment with a decision.
    Supports two target types:
      - target_raw_record_id: compares two raw records against each other.
      - target_canonical_id: compares a raw record against an already-merged
        CanonicalInstitution (its aggregate name/domain/branches/contacts).
    """
    if candidate.target_raw_record_id:
        assessment = await _score_against_raw_record(session, candidate)
    elif candidate.target_canonical_id:
        assessment = await _score_against_canonical(session, candidate)
    else:
        raise ValueError("ResolutionCandidate has neither target_raw_record_id nor target_canonical_id")

    session.add(assessment)
    return assessment


async def _score_against_raw_record(session: AsyncSession, candidate: ResolutionCandidate) -> MatchAssessment:
    # Fetch both records
    stmt = select(RawSourceRecord).where(
        RawSourceRecord.id.in_([candidate.raw_record_id, candidate.target_raw_record_id])
    )
    result = await session.execute(stmt)
    records = {r.id: r for r in result.scalars()}

    source = records[candidate.raw_record_id]
    target = records[candidate.target_raw_record_id]

    # 1. Evaluate Phone Match
    phone_match = False
    if source.normalized_phone and target.normalized_phone:
        phone_match = (source.normalized_phone == target.normalized_phone)

    # 2. Evaluate Domain Match
    domain_match = False
    if source.normalized_domain and target.normalized_domain:
        domain_match = (source.normalized_domain == target.normalized_domain)

    # 3. Evaluate Name Similarity and Geographic Distance
    sim_dist_stmt = select(
        func.similarity(source.normalized_name, target.normalized_name).label("sim"),
        ST_Distance(source.location, target.location).label("dist")
    )
    res = await session.execute(sim_dist_stmt)
    sim, dist = res.one()

    name_similarity = float(sim) if sim is not None else 0.0
    distance_meters = float(dist) if dist is not None else None

    total_score, decision = _decide(name_similarity, distance_meters, phone_match, domain_match)

    return MatchAssessment(
        candidate_id=candidate.id,
        name_similarity=name_similarity,
        distance_meters=distance_meters,
        phone_match=phone_match,
        domain_match=domain_match,
        total_score=total_score,
        decision=decision
    )


async def _score_against_canonical(session: AsyncSession, candidate: ResolutionCandidate) -> MatchAssessment:
    source = await session.get(RawSourceRecord, candidate.raw_record_id)

    institution_stmt = select(CanonicalInstitution).options(
        selectinload(CanonicalInstitution.branches),
        selectinload(CanonicalInstitution.contact_points),
    ).where(CanonicalInstitution.id == candidate.target_canonical_id)
    institution = (await session.execute(institution_stmt)).scalar_one()

    # 1. Evaluate Phone Match against any phone ContactPoint on the institution
    phone_match = False
    if source.normalized_phone:
        institution_phones = {
            cp.contact_value for cp in institution.contact_points if cp.contact_type == "phone"
        }
        phone_match = source.normalized_phone in institution_phones

    # 2. Evaluate Domain Match
    domain_match = False
    if source.normalized_domain and institution.domain:
        domain_match = (source.normalized_domain == institution.domain)

    # 3. Evaluate Name Similarity against the canonical name
    name_similarity = 0.0
    if source.normalized_name and institution.canonical_name:
        sim_stmt = select(func.similarity(source.normalized_name, institution.canonical_name))
        sim = (await session.execute(sim_stmt)).scalar()
        name_similarity = float(sim) if sim is not None else 0.0

    # 4. Evaluate Geographic Distance: closest branch to the source location
    distance_meters = None
    branch_ids = [b.id for b in institution.branches if b.location is not None]
    if source.location is not None and branch_ids:
        dist_stmt = select(func.min(ST_Distance(source.location, Branch.location))).where(
            Branch.id.in_(branch_ids)
        )
        dist = (await session.execute(dist_stmt)).scalar()
        distance_meters = float(dist) if dist is not None else None

    total_score, decision = _decide(name_similarity, distance_meters, phone_match, domain_match)

    return MatchAssessment(
        candidate_id=candidate.id,
        name_similarity=name_similarity,
        distance_meters=distance_meters,
        phone_match=phone_match,
        domain_match=domain_match,
        total_score=total_score,
        decision=decision
    )
