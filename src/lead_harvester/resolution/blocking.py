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

# Relative strength of each blocking strategy as evidence, lowest = strongest.
# geo_name (matching name AND physical proximity) is far more discriminating
# than a bare phone match (routinely shared across an entire franchise's
# unrelated branches) or a bare domain match (a shared portal/CMS domain).
# Used to pick which sibling to keep as the representative for an
# already-canonicalized institution when several match -- keeping an
# arbitrary (e.g. first-in-DB-order) sibling instead could discard the one
# match that actually carries strong evidence in favor of a weaker one,
# understating the eventual score_candidate result.
_STRATEGY_PRIORITY = {"geo_name": 0, "domain": 1, "phone": 2}


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
    unboundedly with repeated ingestion. The kept representative is the one
    matched via the STRONGEST strategy (see _STRATEGY_PRIORITY), not merely
    whichever the DB happened to return first -- an arbitrary weak (phone)
    match could otherwise shadow a same-institution sibling that actually
    matched on name+location, understating the eventual score. Still-
    unresolved matches are never deduplicated this way -- each is a genuine,
    independent candidate that may need its own review/merge decision.
    """
    # record_id -> the strongest strategy that matched it, across all three
    # blocking queries (a record can qualify via more than one).
    matched_strategy: dict[uuid.UUID, str] = {}

    def _note_matches(matched_ids: list[uuid.UUID], strategy: str) -> None:
        for rid in matched_ids:
            current = matched_strategy.get(rid)
            if current is None or _STRATEGY_PRIORITY[strategy] < _STRATEGY_PRIORITY[current]:
                matched_strategy[rid] = strategy

    # Strategy 1: Exact Phone Match
    if record.normalized_phone:
        stmt = select(RawSourceRecord.id).where(
            RawSourceRecord.normalized_phone == record.normalized_phone,
            RawSourceRecord.id != record.id,
        )
        result = await session.execute(stmt)
        _note_matches(list(result.scalars()), "phone")

    # Strategy 2: Exact Domain Match
    if record.normalized_domain:
        stmt = select(RawSourceRecord.id).where(
            RawSourceRecord.normalized_domain == record.normalized_domain,
            RawSourceRecord.id != record.id,
        )
        result = await session.execute(stmt)
        _note_matches(list(result.scalars()), "domain")

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
        _note_matches(list(result.scalars()), "geo_name")

    if not matched_strategy:
        return []

    canonical_by_record = await _canonical_ids_by_raw_record(session, list(matched_strategy))

    candidates = []
    best_per_canonical: dict[uuid.UUID, uuid.UUID] = {}
    for rid, strategy in matched_strategy.items():
        canonical_id = canonical_by_record.get(rid)
        if canonical_id is None:
            # Not yet resolved -- always its own independent candidate.
            candidates.append(
                ResolutionCandidate(
                    raw_record_id=record.id,
                    target_raw_record_id=rid,
                    blocking_strategy=strategy,
                )
            )
            continue

        current_best = best_per_canonical.get(canonical_id)
        if current_best is None or (
            _STRATEGY_PRIORITY[strategy] < _STRATEGY_PRIORITY[matched_strategy[current_best]]
        ):
            best_per_canonical[canonical_id] = rid

    for rid in best_per_canonical.values():
        candidates.append(
            ResolutionCandidate(
                raw_record_id=record.id,
                target_raw_record_id=rid,
                blocking_strategy=matched_strategy[rid],
            )
        )

    return candidates
