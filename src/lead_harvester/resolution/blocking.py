from geoalchemy2 import Geography
from geoalchemy2.functions import ST_DWithin
from sqlalchemy import cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.resolution import ResolutionCandidate
from lead_harvester.models.source import RawSourceRecord

# Trigram similarity threshold (0 to 1). pg_trgm default is 0.3
NAME_SIMILARITY_THRESHOLD = 0.4
# Distance threshold in meters (e.g. 500 meters)
GEOGRAPHIC_DISTANCE_METERS = 500


async def generate_candidates(
    session: AsyncSession, record: RawSourceRecord
) -> list[ResolutionCandidate]:
    """
    Finds potential matches in the database for a given raw record using blocking strategies.
    Generates ResolutionCandidate objects (but does not commit them).
    """
    candidates = []
    seen_ids = set()

    # Strategy 1: Exact Phone Match
    if record.normalized_phone:
        stmt = select(RawSourceRecord).where(
            RawSourceRecord.normalized_phone == record.normalized_phone,
            RawSourceRecord.id != record.id,
        )
        result = await session.execute(stmt)
        for row in result.scalars():
            if row.id not in seen_ids:
                seen_ids.add(row.id)
                candidates.append(
                    ResolutionCandidate(
                        raw_record_id=record.id,
                        target_raw_record_id=row.id,
                        blocking_strategy="phone",
                    )
                )

    # Strategy 2: Exact Domain Match
    if record.normalized_domain:
        stmt = select(RawSourceRecord).where(
            RawSourceRecord.normalized_domain == record.normalized_domain,
            RawSourceRecord.id != record.id,
        )
        result = await session.execute(stmt)
        for row in result.scalars():
            if row.id not in seen_ids:
                seen_ids.add(row.id)
                candidates.append(
                    ResolutionCandidate(
                        raw_record_id=record.id,
                        target_raw_record_id=row.id,
                        blocking_strategy="domain",
                    )
                )

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
        stmt = select(RawSourceRecord).where(
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
        for row in result.scalars():
            if row.id not in seen_ids:
                seen_ids.add(row.id)
                candidates.append(
                    ResolutionCandidate(
                        raw_record_id=record.id,
                        target_raw_record_id=row.id,
                        blocking_strategy="geo_name",
                    )
                )

    return candidates
