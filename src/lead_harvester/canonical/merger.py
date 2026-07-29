import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.canonical import (
    Branch,
    CanonicalInstitution,
    ContactPoint,
    OperatingStatus,
)
from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.source import RawSourceRecord, SourceType

# Google Places' response (the only live raw-record source today) does not
# request structured address components, only a free-text formattedAddress --
# so city/country_code are genuinely unknown at merge time. Matches the same
# sentinel values the city/country_code backfill migration used.
_UNKNOWN_CITY = "Unknown"
_UNKNOWN_COUNTRY_CODE = "XX"


def display_fields(record: RawSourceRecord) -> dict[str, str | None]:
    """
    Extracts name/address/website/institution_type in a source-shape-aware
    way. RawSourceRecord.raw_payload's keys differ entirely by source_type
    (Google Places' payload is the raw Places API response; the web
    crawler's is dataclasses.asdict(Lead); manual entries mirror
    ManualLeadIn) -- reading a fixed (Google-Places-shaped) set of keys
    regardless of source silently produced blank addresses and null
    websites for every non-Google-Places record.
    """
    payload = record.raw_payload or {}

    if record.source_type == SourceType.GOOGLE_PLACES:
        name = record.normalized_name or payload.get("displayName", {}).get("text", "Unknown")
        return {
            "name": name,
            "address": payload.get("formattedAddress", ""),
            "website": payload.get("websiteUri"),
            "email": None,
            "institution_type": payload.get("primaryType", ""),
        }

    if record.source_type == SourceType.WEBSITE:
        name = record.normalized_name or payload.get("name") or "Unknown"
        return {
            "name": name,
            "address": payload.get("location") or "",
            # normalized_domain is a bare host ("example.edu") used for
            # blocking/matching -- prefer the full origin from raw_payload
            # ("https://example.edu") as the actual website value, since
            # normalized_domain is truthy whenever a website exists at all
            # and would otherwise always shadow the real URL.
            "website": payload.get("website") or record.normalized_domain,
            "email": payload.get("email") or None,
            "institution_type": "",
        }

    if record.source_type == SourceType.MANUAL:
        name = record.normalized_name or payload.get("institution_name", "Unknown")
        return {
            "name": name,
            "address": payload.get("address", ""),
            "website": payload.get("website"),
            "email": None,
            "institution_type": payload.get("institution_type", ""),
        }

    # No connector exists yet for any other SourceType (telegram/linkedin/
    # yandex/apple_maps) -- fall back to the normalized index fields only
    # rather than guessing at an unknown raw_payload shape.
    return {
        "name": record.normalized_name or "Unknown",
        "address": "",
        "website": record.normalized_domain,
        "email": None,
        "institution_type": "",
    }


def _provider_ids_for(records: list[RawSourceRecord]) -> dict[str, list[str]]:
    # Keyed by source_type, valued as a LIST of source_ids -- two records of
    # the same source_type folded into one branch (e.g. two Google Places
    # hits confirmed to be the same physical location) must each keep their
    # own source_id. A bare str value would let the second overwrite the
    # first, and a later run rediscovering the overwritten place could never
    # find this branch via find_branch_for_raw_record, silently splitting
    # one physical location into two Branch rows.
    provider_ids: dict[str, list[str]] = {}
    for r in records:
        provider_ids.setdefault(r.source_type.value, []).append(r.source_id)
    return provider_ids


def _build_branch(
    records: list[RawSourceRecord], institution_id: uuid.UUID, *, branch_name: str
) -> Branch:
    primary = records[0]
    fields = display_fields(primary)
    return Branch(
        institution_id=institution_id,
        branch_name=branch_name,
        address=fields["address"] or "",
        city=_UNKNOWN_CITY,
        country_code=_UNKNOWN_COUNTRY_CODE,
        location=primary.location,
        provider_ids=_provider_ids_for(records),
    )


def _create_branches(
    session: AsyncSession,
    institution: CanonicalInstitution,
    records: list[RawSourceRecord],
    *,
    same_location: bool,
) -> list[Branch]:
    if same_location:
        branch = _build_branch(records, institution.id, branch_name="Main Campus")
        session.add(branch)
        return [branch]

    branches = []
    for i, record in enumerate(records):
        name = "Main Campus" if i == 0 else "Additional Campus"
        branch = _build_branch([record], institution.id, branch_name=name)
        session.add(branch)
        branches.append(branch)
    return branches


async def _find_contact_point(
    session: AsyncSession, institution_id: uuid.UUID, contact_type: str, contact_value: str
) -> ContactPoint | None:
    stmt = select(ContactPoint).where(
        ContactPoint.institution_id == institution_id,
        ContactPoint.contact_type == contact_type,
        ContactPoint.contact_value == contact_value,
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def _add_contacts_and_provenance(
    session: AsyncSession, institution: CanonicalInstitution, record: RawSourceRecord
) -> None:
    # Written unconditionally (not just when a phone is present) so every
    # merged record can later be traced back to the institution it
    # contributed to via find_canonical_for_raw_record, regardless of which
    # fields it happened to supply.
    session.add(
        FieldProvenance(
            canonical_id=institution.id,
            raw_record_id=record.id,
            field_name="branch_membership",
            asserted_value=record.source_id,
            assertion_trust=1.0,
        )
    )

    await _add_contact_if_present(
        session, institution, record, contact_type="phone", contact_value=record.normalized_phone
    )
    email = display_fields(record).get("email")
    await _add_contact_if_present(
        session, institution, record, contact_type="email", contact_value=email
    )


async def _add_contact_if_present(
    session: AsyncSession,
    institution: CanonicalInstitution,
    record: RawSourceRecord,
    *,
    contact_type: str,
    contact_value: str | None,
) -> None:
    if not contact_value:
        return

    # Overlapping ingestion (e.g. repeated Google Places queries hitting the
    # same place, or a later run re-discovering the same institution) would
    # otherwise insert a duplicate ContactPoint every time -- reuse the
    # existing one (still recording this record's own provenance link to
    # it) instead.
    existing = await _find_contact_point(session, institution.id, contact_type, contact_value)
    if existing is None:
        session.add(
            ContactPoint(
                institution_id=institution.id,
                contact_type=contact_type,
                contact_value=contact_value,
            )
        )
    session.add(
        FieldProvenance(
            canonical_id=institution.id,
            raw_record_id=record.id,
            field_name=f"contact_{contact_type}",
            asserted_value=contact_value,
            assertion_trust=1.0,
        )
    )


async def merge_records(
    session: AsyncSession, raw_records: list[RawSourceRecord], *, same_location: bool = False
) -> CanonicalInstitution:
    """
    Takes a group of raw records that have been assessed as a MERGE,
    and synthesizes them into a single pristine CanonicalInstitution.

    same_location=True collapses every record into a single shared Branch
    (they describe the exact same physical location -- e.g. score_candidate's
    MatchDecision.MERGE, which only fires when name and geographic distance
    both confirm it). same_location=False (the default) gives each record
    its own Branch under the shared institution -- the common "first time
    seeing this institution" case, and the "distinct physical locations of
    the same institution" case.
    """
    if not raw_records:
        raise ValueError("Cannot merge empty record list")

    # In a real conflict-handling scenario, we would use a voting system
    # weighted by the trust score of the source. For now, we take the
    # most complete/recent record as primary for name/domain/website/type.
    primary_record = raw_records[0]
    fields = display_fields(primary_record)

    institution = CanonicalInstitution(
        canonical_name=fields["name"],
        institution_type=fields["institution_type"] or "",
        domain=primary_record.normalized_domain,
        website=fields["website"],
        status=OperatingStatus.OPERATIONAL,
        confidence_score=len(raw_records) * 10.0,  # simple confidence metric
    )
    session.add(institution)

    # We must flush to get the UUID for the institution so we can link Branches and Provenance
    await session.flush()

    # Record Provenance for the core fields
    session.add(
        FieldProvenance(
            canonical_id=institution.id,
            raw_record_id=primary_record.id,
            field_name="canonical_name",
            asserted_value=fields["name"],
            assertion_trust=1.0,
        )
    )

    _create_branches(session, institution, raw_records, same_location=same_location)
    for record in raw_records:
        await _add_contacts_and_provenance(session, institution, record)

    return institution


async def find_canonical_for_raw_record(
    session: AsyncSession, raw_record_id: uuid.UUID
) -> uuid.UUID | None:
    """
    Looks up whether a raw record has already contributed to a canonical
    institution, via the FieldProvenance "branch_membership" link
    merge_records always writes -- unconditionally, regardless of whether
    the record has a phone number.
    """
    stmt = (
        select(FieldProvenance.canonical_id)
        .where(FieldProvenance.raw_record_id == raw_record_id)
        .limit(1)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def find_branch_for_raw_record(
    session: AsyncSession, institution_id: uuid.UUID, record: RawSourceRecord
) -> Branch | None:
    """
    Finds the specific Branch a raw record belongs to. Branch has no direct
    FK to the raw records that produced it -- only provider_ids, keyed by
    source_type with a list of every contributing source_id -- so this loads
    the institution's (typically small) branch set and matches in Python
    rather than relying on a JSONB operator. Returns None if no match is
    found -- callers should treat that as "create a new branch" rather than
    guessing which existing one to enrich.
    """
    stmt = select(Branch).where(Branch.institution_id == institution_id)
    result = await session.execute(stmt)
    for branch in result.scalars():
        if record.source_id in branch.provider_ids.get(record.source_type.value, []):
            return branch
    return None


async def attach_record_to_institution(
    session: AsyncSession,
    record: RawSourceRecord,
    institution: CanonicalInstitution,
    *,
    target_branch: Branch | None = None,
) -> Branch:
    """
    Attaches one more raw record's evidence to an institution that already
    exists -- the "one more record for something already resolved" path, as
    opposed to merge_records which always creates a brand new institution.

    target_branch=None creates a new Branch under the institution (a
    distinct physical location of the same institution). target_branch=<a
    Branch> enriches that branch in place instead (this record describes the
    same branch).
    """
    if target_branch is not None:
        fields = display_fields(record)
        if not target_branch.address and fields["address"]:
            target_branch.address = fields["address"]
        # provider_ids is a plain JSONB column (no MutableDict tracking), so
        # mutating the existing dict/list in place would never be detected
        # as a change -- reassign a new dict (with a new list for this
        # source_type) so the attribute-set event actually marks the branch
        # dirty. Appending to the list (not overwriting the key) so this
        # doesn't lose a previously-recorded source_id for the same
        # source_type -- see _provider_ids_for's docstring.
        source_type = record.source_type.value
        existing_ids = list(target_branch.provider_ids.get(source_type, []))
        if record.source_id not in existing_ids:
            existing_ids.append(record.source_id)
        target_branch.provider_ids = {**target_branch.provider_ids, source_type: existing_ids}
        branch = target_branch
    else:
        branch = _build_branch([record], institution.id, branch_name="Additional Campus")
        session.add(branch)

    await _add_contacts_and_provenance(session, institution, record)
    institution.confidence_score += 10.0

    return branch
