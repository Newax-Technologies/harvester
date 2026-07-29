from geoalchemy2.functions import ST_Distance
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.resolution import MatchAssessment, MatchDecision, ResolutionCandidate
from lead_harvester.models.source import RawSourceRecord


async def score_candidate(session: AsyncSession, candidate: ResolutionCandidate) -> MatchAssessment:
    """
    Evaluates a candidate pairing and returns a MatchAssessment with a decision.
    Currently compares two raw records (target_raw_record_id).
    """
    if not candidate.target_raw_record_id:
        raise NotImplementedError("Canonical target scoring not yet implemented")

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
        phone_match = source.normalized_phone == target.normalized_phone

    # 2. Evaluate Domain Match
    domain_match = False
    if source.normalized_domain and target.normalized_domain:
        domain_match = source.normalized_domain == target.normalized_domain

    # 3. Evaluate Name Similarity and Geographic Distance
    # Since these require DB functions, we can execute a quick query, or compute in python if simple.
    # We'll use the DB to calculate similarity and distance.
    sim_dist_stmt = select(
        func.similarity(source.normalized_name, target.normalized_name).label("sim"),
        ST_Distance(source.location, target.location).label("dist"),
    )
    res = await session.execute(sim_dist_stmt)
    sim, dist = res.one()

    name_similarity = float(sim) if sim is not None else 0.0
    distance_meters = float(dist) if dist is not None else None

    # --- Scoring Matrix & Decision Logic ---
    decision = MatchDecision.REJECT
    total_score = 0.0

    # Base scoring
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

    # Decision Rules
    if name_similarity > 0.8 and distance_meters is not None and distance_meters < 100:
        # Same name, same location -> Definitely the same entity (MERGE)
        decision = MatchDecision.MERGE
    elif domain_match and name_similarity > 0.8:
        # An exact website-domain match plus a strong name match is too
        # confident to auto-dismiss as LINK_ONLY (unlike phone_match alone,
        # which franchises commonly share across genuinely distinct
        # locations) but can't auto-MERGE without geographic confirmation --
        # e.g. a web-crawled record has no coordinates at all (location is
        # always None), so cross-source matches never reach the MERGE branch
        # above. Flag for human review instead of silently treating it as
        # confidently distinct.
        decision = MatchDecision.PENDING
    elif phone_match or domain_match:
        # Shared contact details, but potentially different physical locations/names.
        # This prevents merging a franchise network into a single school.
        decision = MatchDecision.LINK_ONLY
    elif total_score >= 60:
        # >= not >: the highest score reachable without tripping either MERGE
        # (needs name>0.8 AND distance<100) or LINK_ONLY (needs phone/domain)
        # is exactly 60 (one "secondary" bucket each from name and distance,
        # e.g. name in (0.5,0.8]+distance<50, or name>0.8+distance in
        # [100,200)) -- a strict `> 60` made this branch unreachable and the
        # review queue would never receive a candidate.
        # High overall confidence but lacking definitive proof
        decision = MatchDecision.PENDING

    assessment = MatchAssessment(
        candidate_id=candidate.id,
        name_similarity=name_similarity,
        distance_meters=distance_meters,
        phone_match=phone_match,
        domain_match=domain_match,
        total_score=total_score,
        decision=decision,
    )

    session.add(assessment)
    return assessment
