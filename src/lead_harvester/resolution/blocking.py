import uuid

from geoalchemy2 import Geography
from geoalchemy2.functions import ST_DWithin
from sqlalchemy import cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.resolution import ResolutionCandidate
from lead_harvester.models.source import RawSourceRecord

# Trigram similarity threshold (0 to 1). pg_trgm default is 0.3
NAME_SIMILARITY_THRESHOLD = 0.4
# Distance threshold in meters (e.g. 500 meters)
GEOGRAPHIC_DISTANCE_METERS = 500


async def _canonical_ids_by_raw_record(
    session: AsyncSession, raw_record_ids: list[uuid.UUID]
) -> dict[uuid.UUID, uuid.UUID]:
    """
    Batched version of canonical/merger.py's find_canonical_for_raw_record,
    for every id in raw_record_ids at once (one query instead of one per
    row). A raw record can have several FieldProvenance rows (one per
    field it asserted) that all share the same canonical_id, so any one is
    equally valid -- building the dict just overwrites with an identical
    value for the extras.
    """
    if not raw_record_ids:
        return {}
    stmt = select(FieldProvenance.raw_record_id, FieldProvenance.canonical_id).where(
        FieldProvenance.raw_record_id.in_(raw_record_ids)
    )
    result = await session.execute(stmt)
    return dict(result.all())


async def generate_candidates(
    session: AsyncSession, record: RawSourceRecord
) -> list[ResolutionCandidate]:
    """
    Finds potential matches in the database for a given raw record using blocking strategies.
    Generates ResolutionCandidate objects (but does not commit them).

    When a matched record already belongs to a canonical institution (e.g.
    rediscovering a popular Google Place, or many franchise branches sharing
    one phone number), only ONE such match per distinct institution is kept
    -- any single one is enough for resolve_incoming_record to identify and
    attach to that institution via find_canonical_for_raw_record, so scoring
    (and persisting a permanent ResolutionCandidate/MatchAssessment row for)
    every other already-represented sibling is pure waste that grows
    unboundedly with repeated ingestion. Still-unresolved matches are never
    deduplicated this way -- each is a genuine, independent candidate that
    may need its own review/merge decision.
    """
    candidates = []
    seen_ids: set[uuid.UUID] = set()
    seen_canonical_ids: set[uuid.UUID] = set()

    async def _add_matches(matched_ids: list[uuid.UUID], strategy: str) -> None:
        fresh_ids = [rid for rid in matched_ids if rid not in seen_ids]
        canonical_by_record = await _canonical_ids_by_raw_record(session, fresh_ids)
        for rid in fresh_ids:
            seen_ids.add(rid)
            canonical_id = canonical_by_record.get(rid)
            if canonical_id is not None:
                if canonical_id in seen_canonical_ids:
                    continue
                seen_canonical_ids.add(canonical_id)
            candidates.append(
                ResolutionCandidate(
                    raw_record_id=record.id,
                    target_raw_record_id=rid,
                    blocking_strategy=strategy,
                )
            )

    # Strategy 1: Exact Phone Match
    if record.normalized_phone:
        stmt = select(RawSourceRecord.id).where(
            RawSourceRecord.normalized_phone == record.normalized_phone,
            RawSourceRecord.id != record.id,
        )
        result = await session.execute(stmt)
        await _add_matches(list(result.scalars()), "phone")

    # Strategy 2: Exact Domain Match
    if record.normalized_domain:
        stmt = select(RawSourceRecord.id).where(
            RawSourceRecord.normalized_domain == record.normalized_domain,
            RawSourceRecord.id != record.id,
        )
        result = await session.execute(stmt)
        await _add_matches(list(result.scalars()), "domain")

    # Strategy 3: Geographic Proximity + Name Similarity
    if record.location is not None and record.normalized_name:
        # We need the pg_trgm '%' operator (similarity). In SQLAlchemy, we can use func.similarity
        # or the custom operator.

        # record.location may still be the raw WKT string set at
        # construction time (not yet reloaded from the DB as a WKBElement)
        # when this runs immediately after creating a new record -- cast it
        # explicitly so it binds as a geography value, not a bare varchar
        # ("function st_dwithin(geography, character varying, ...) does not
        # exist" otherwise).
        # We only want records that are physically close AND have similar names.
        stmt = select(RawSourceRecord.id).where(
            RawSourceRecord.id != record.id,
            RawSourceRecord.location.is_not(None),
            ST_DWithin(
                RawSourceRecord.location,
                cast(record.location, Geography),
                GEOGRAPHIC_DISTANCE_METERS,
            ),
            func.similarity(RawSourceRecord.normalized_name, record.normalized_name)
            >= NAME_SIMILARITY_THRESHOLD,
        )
        result = await session.execute(stmt)
        await _add_matches(list(result.scalars()), "geo_name")

    return candidates
