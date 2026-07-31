import uuid
from typing import List

from sqlalchemy import or_, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.functions import ST_DWithin

from lead_harvester.models.source import RawSourceRecord
from lead_harvester.models.canonical import CanonicalInstitution, Branch, ContactPoint
from lead_harvester.models.resolution import ResolutionCandidate

# Trigram similarity threshold (0 to 1). pg_trgm default is 0.3
NAME_SIMILARITY_THRESHOLD = 0.4
# Distance threshold in meters (e.g. 500 meters)
GEOGRAPHIC_DISTANCE_METERS = 500

async def generate_candidates(session: AsyncSession, record: RawSourceRecord) -> List[ResolutionCandidate]:
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
            RawSourceRecord.id != record.id
        )
        result = await session.execute(stmt)
        for row in result.scalars():
            if row.id not in seen_ids:
                seen_ids.add(row.id)
                candidates.append(ResolutionCandidate(
                    raw_record_id=record.id,
                    target_raw_record_id=row.id,
                    blocking_strategy="phone"
                ))
                
    # Strategy 2: Exact Domain Match
    if record.normalized_domain:
        stmt = select(RawSourceRecord).where(
            RawSourceRecord.normalized_domain == record.normalized_domain,
            RawSourceRecord.id != record.id
        )
        result = await session.execute(stmt)
        for row in result.scalars():
            if row.id not in seen_ids:
                seen_ids.add(row.id)
                candidates.append(ResolutionCandidate(
                    raw_record_id=record.id,
                    target_raw_record_id=row.id,
                    blocking_strategy="domain"
                ))

    # Strategy 3: Geographic Proximity + Name Similarity
    if record.location is not None and record.normalized_name:
        # We need the pg_trgm '%' operator (similarity). In SQLAlchemy, we can use func.similarity
        # or the custom operator.
        
        # We only want records that are physically close AND have similar names.
        stmt = select(RawSourceRecord).where(
            RawSourceRecord.id != record.id,
            RawSourceRecord.location.is_not(None),
            ST_DWithin(RawSourceRecord.location, record.location, GEOGRAPHIC_DISTANCE_METERS),
            func.similarity(RawSourceRecord.normalized_name, record.normalized_name) >= NAME_SIMILARITY_THRESHOLD
        )
        result = await session.execute(stmt)
        for row in result.scalars():
            if row.id not in seen_ids:
                seen_ids.add(row.id)
                candidates.append(ResolutionCandidate(
                    raw_record_id=record.id,
                    target_raw_record_id=row.id,
                    blocking_strategy="geo_name"
                ))

    # Strategies 4-6: block against already-merged CanonicalInstitutions, so new
    # incoming records can be linked/merged into entities that already exist
    # instead of only ever matching other unresolved raw records.
    seen_canonical_ids = set()

    # Strategy 4: Exact Domain Match against a CanonicalInstitution
    if record.normalized_domain:
        stmt = select(CanonicalInstitution.id).where(
            CanonicalInstitution.domain == record.normalized_domain
        )
        result = await session.execute(stmt)
        for institution_id in result.scalars():
            if institution_id not in seen_canonical_ids:
                seen_canonical_ids.add(institution_id)
                candidates.append(ResolutionCandidate(
                    raw_record_id=record.id,
                    target_canonical_id=institution_id,
                    blocking_strategy="canonical_domain"
                ))

    # Strategy 5: Exact Phone Match against a CanonicalInstitution's ContactPoints
    if record.normalized_phone:
        stmt = select(ContactPoint.institution_id).where(
            ContactPoint.contact_type == "phone",
            ContactPoint.contact_value == record.normalized_phone
        )
        result = await session.execute(stmt)
        for institution_id in result.scalars():
            if institution_id not in seen_canonical_ids:
                seen_canonical_ids.add(institution_id)
                candidates.append(ResolutionCandidate(
                    raw_record_id=record.id,
                    target_canonical_id=institution_id,
                    blocking_strategy="canonical_phone"
                ))

    # Strategy 6: Geographic Proximity + Name Similarity against a CanonicalInstitution's Branches
    if record.location is not None and record.normalized_name:
        stmt = (
            select(Branch.institution_id)
            .join(CanonicalInstitution, CanonicalInstitution.id == Branch.institution_id)
            .where(
                Branch.location.is_not(None),
                ST_DWithin(Branch.location, record.location, GEOGRAPHIC_DISTANCE_METERS),
                func.similarity(CanonicalInstitution.canonical_name, record.normalized_name) >= NAME_SIMILARITY_THRESHOLD
            )
        )
        result = await session.execute(stmt)
        for institution_id in result.scalars():
            if institution_id not in seen_canonical_ids:
                seen_canonical_ids.add(institution_id)
                candidates.append(ResolutionCandidate(
                    raw_record_id=record.id,
                    target_canonical_id=institution_id,
                    blocking_strategy="canonical_geo_name"
                ))

    return candidates
