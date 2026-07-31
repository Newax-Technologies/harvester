from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from lead_harvester.models.source import RawSourceRecord, SourceType
from lead_harvester.models.canonical import CanonicalInstitution, Branch, ContactPoint, OperatingStatus
from lead_harvester.models.compliance import ConsentBasis, IdentifierType
from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.resolution import MatchAssessment, MatchDecision
from lead_harvester.compliance.suppression import SuppressionService

# Public business directories/websites give a straightforward public-listing
# basis; manual entry is first-party. Scraped social sources (Telegram,
# LinkedIn) are intentionally left unmapped -> ConsentBasis.UNKNOWN, since
# they need explicit human review before being treated as cleared for outreach.
_CONSENT_BASIS_BY_SOURCE_TYPE = {
    SourceType.GOOGLE_PLACES: ConsentBasis.PUBLIC_DIRECTORY,
    SourceType.YANDEX: ConsentBasis.PUBLIC_DIRECTORY,
    SourceType.APPLE_MAPS: ConsentBasis.PUBLIC_DIRECTORY,
    SourceType.WEBSITE: ConsentBasis.PUBLIC_DIRECTORY,
    SourceType.MANUAL: ConsentBasis.OWNED_DATA,
}

async def merge_records(session: AsyncSession, raw_records: List[RawSourceRecord]) -> CanonicalInstitution:
    """
    Takes a group of raw records that have been assessed as a MERGE,
    and synthesizes them into a single pristine CanonicalInstitution.
    """
    if not raw_records:
        raise ValueError("Cannot merge empty record list")
        
    # Create the base institution.
    # In a real conflict-handling scenario, we would use a voting system
    # weighted by the trust score of the source. For now, we take the most complete/recent.
    # Sort by the presence of data, or just take the first as the primary for names.
    primary_record = raw_records[0]
    
    canonical_name = primary_record.normalized_name or primary_record.raw_payload.get("displayName", {}).get("text", "Unknown")
    domain = primary_record.normalized_domain
    website = primary_record.raw_payload.get("websiteUri")
    
    institution = CanonicalInstitution(
        canonical_name=canonical_name,
        institution_type=primary_record.raw_payload.get("primaryType", ""),
        domain=domain,
        website=website,
        status=OperatingStatus.OPERATIONAL,
        confidence_score=len(raw_records) * 10.0 # simple confidence metric
    )
    session.add(institution)
    
    # We must flush to get the UUID for the institution so we can link Branches and Provenance
    await session.flush()
    
    # Record Provenance for the core fields
    session.add(FieldProvenance(
        canonical_id=institution.id,
        raw_record_id=primary_record.id,
        field_name="canonical_name",
        asserted_value=canonical_name,
        assertion_trust=1.0
    ))
    
    # Process Branches (Physical Locations) and Contacts
    for record in raw_records:
        # 1. Create a Branch for this location
        address = record.raw_payload.get("formattedAddress", "")
        branch = Branch(
            institution_id=institution.id,
            branch_name="Main Campus" if record == primary_record else "Additional Campus",
            address=address,
            location=record.location,
            provider_ids={record.source_type.value: record.source_id}
        )
        session.add(branch)
        
        # 2. Extract and link ContactPoints (skip anything on the suppression list,
        # so a deleted/opted-out identifier doesn't get silently re-materialized)
        phone = record.normalized_phone
        if phone and not await SuppressionService.is_suppressed(session, IdentifierType.PHONE, phone):
            contact = ContactPoint(
                institution_id=institution.id,
                contact_type="phone",
                contact_value=phone,
                consent_basis=_CONSENT_BASIS_BY_SOURCE_TYPE.get(record.source_type, ConsentBasis.UNKNOWN),
            )
            session.add(contact)
            
            # Provenance for the phone
            session.add(FieldProvenance(
                canonical_id=institution.id,
                raw_record_id=record.id,
                field_name="contact_phone",
                asserted_value=phone,
                assertion_trust=1.0
            ))

    return institution
