import uuid

from geoalchemy2 import Geography
from geoalchemy2.functions import ST_Distance, ST_DWithin
from sqlalchemy import cast, func, literal, select
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


class _MatchInfo:
    """
    What generate_candidates knows about one matched record: the strongest
    strategy it qualified under, plus its actual distance/name similarity
    to the incoming record -- used to break ties WITHIN a shared strategy
    tier. Two matches aren't equally good just because they share a
    strategy label: among two domain-only matches, one with an exact name
    match is much stronger evidence than one with a completely unrelated
    name, and among two geo_name matches, a 490m/0.4-similarity match is
    much weaker than a 10m/1.0-similarity one. Computed uniformly for every
    matched record regardless of which strategy(ies) surfaced it, so this
    tiebreak isn't only available within the geo_name tier.
    """

    __slots__ = ("distance_meters", "name_similarity", "strategy")

    def __init__(
        self,
        strategy: str,
        distance_meters: float | None = None,
        name_similarity: float | None = None,
    ) -> None:
        self.strategy = strategy
        self.distance_meters = distance_meters
        self.name_similarity = name_similarity

    def sort_key(self) -> tuple[int, float, float]:
        # name_similarity ranks before distance -- it's the dominant signal
        # across every branch of scoring.py's decision logic (the MERGE
        # gate requires similarity>0.8 explicitly; the phone/domain
        # PENDING-vs-LINK_ONLY split is ALSO purely gated on similarity>0.8;
        # distance only ever matters as MERGE's secondary confirming
        # condition). Ranking distance first would let a geographically
        # close-by-coincidence but otherwise unrelated match (finite
        # distance, low similarity) outrank an exact-name match that simply
        # has no location data (distance=None), keeping the worse
        # representative (would score LINK_ONLY) over the better one
        # (would score PENDING and actually surface for review).
        return (
            _STRATEGY_PRIORITY[self.strategy],
            -(self.name_similarity if self.name_similarity is not None else 0.0),
            self.distance_meters if self.distance_meters is not None else float("inf"),
        )

    def is_better_than(self, other: "_MatchInfo") -> bool:
        return self.sort_key() < other.sort_key()


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


async def _quality_for_matches(
    session: AsyncSession, record: RawSourceRecord, raw_record_ids: list[uuid.UUID]
) -> dict[uuid.UUID, tuple[float | None, float | None]]:
    """
    Actual (distance_meters, name_similarity) against `record` for every id
    in raw_record_ids, computed in one query regardless of which blocking
    strategy matched them -- so a tie between two phone-only (or two
    domain-only) matches is still broken by real evidence instead of
    arbitrary DB row order. Either component is None when `record` itself
    lacks the corresponding field (no location, or no normalized_name).
    """
    if not raw_record_ids:
        return {}

    distance_expr = (
        ST_Distance(RawSourceRecord.location, cast(record.location, Geography))
        if record.location is not None
        else literal(None)
    )
    similarity_expr = (
        func.similarity(RawSourceRecord.normalized_name, record.normalized_name)
        if record.normalized_name
        else literal(None)
    )
    stmt = select(RawSourceRecord.id, distance_expr, similarity_expr).where(
        RawSourceRecord.id.in_(raw_record_ids)
    )
    result = await session.execute(stmt)
    return {rid: (distance, similarity) for rid, distance, similarity in result.all()}


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
    with the strongest evidence -- ranked first by strategy (see
    _STRATEGY_PRIORITY), then by actual distance/name-similarity computed
    uniformly for every match (see _MatchInfo/_quality_for_matches) -- not
    merely whichever the DB happened to return first. Still-unresolved
    matches are never deduplicated this way -- each is a genuine,
    independent candidate that may need its own review/merge decision.
    """
    # record_id -> the strongest strategy that matched it, across all three
    # blocking queries (a record can qualify via more than one).
    matched_strategy: dict[uuid.UUID, str] = {}

    def _note_matches(ids, strategy: str) -> None:
        for rid in ids:
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
        record_geog = cast(record.location, Geography)
        similarity_col = func.similarity(RawSourceRecord.normalized_name, record.normalized_name)
        stmt = select(RawSourceRecord.id).where(
            RawSourceRecord.id != record.id,
            RawSourceRecord.location.is_not(None),
            ST_DWithin(RawSourceRecord.location, record_geog, GEOGRAPHIC_DISTANCE_METERS),
            similarity_col >= NAME_SIMILARITY_THRESHOLD,
        )
        result = await session.execute(stmt)
        _note_matches(list(result.scalars()), "geo_name")

    if not matched_strategy:
        return []

    quality = await _quality_for_matches(session, record, list(matched_strategy))
    matched_info: dict[uuid.UUID, _MatchInfo] = {
        rid: _MatchInfo(strategy, *quality.get(rid, (None, None)))
        for rid, strategy in matched_strategy.items()
    }

    canonical_by_record = await _canonical_ids_by_raw_record(session, list(matched_info))

    candidates = []
    best_per_canonical: dict[uuid.UUID, uuid.UUID] = {}
    for rid, info in matched_info.items():
        canonical_id = canonical_by_record.get(rid)
        if canonical_id is None:
            # Not yet resolved -- always its own independent candidate.
            candidates.append(
                ResolutionCandidate(
                    raw_record_id=record.id,
                    target_raw_record_id=rid,
                    blocking_strategy=info.strategy,
                )
            )
            continue

        current_best_id = best_per_canonical.get(canonical_id)
        if current_best_id is None or info.is_better_than(matched_info[current_best_id]):
            best_per_canonical[canonical_id] = rid

    for rid in best_per_canonical.values():
        candidates.append(
            ResolutionCandidate(
                raw_record_id=record.id,
                target_raw_record_id=rid,
                blocking_strategy=matched_info[rid].strategy,
            )
        )

    return candidates
