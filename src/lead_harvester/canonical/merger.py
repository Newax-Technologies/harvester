import uuid
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.canonical import (
    Branch,
    CanonicalInstitution,
    ContactPoint,
    OperatingStatus,
)
from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.source import RawSourceRecord, SourceType
from lead_harvester.resolution.normalize import normalize_phone
from lead_harvester.services.person_candidate_service import resolve_person_candidate
from lead_harvester.verification.confidence import bump_confidence, confidence_for_source_count

# Google Places' response (the only live raw-record source today) does not
# request structured address components, only a free-text formattedAddress --
# so city/country_code are genuinely unknown at merge time. Matches the same
# sentinel values the city/country_code backfill migration used.
_UNKNOWN_CITY = "Unknown"
_UNKNOWN_COUNTRY_CODE = "XX"

_GOOGLE_BUSINESS_STATUS_MAP = {
    "OPERATIONAL": OperatingStatus.OPERATIONAL,
    "CLOSED_TEMPORARILY": OperatingStatus.CLOSED_TEMPORARILY,
    "CLOSED_PERMANENTLY": OperatingStatus.CLOSED_PERMANENTLY,
}


def _operating_status(record: RawSourceRecord) -> OperatingStatus:
    """
    Google Places' response includes a businessStatus field (requested via
    the connector's field mask) that flags CLOSED_TEMPORARILY/
    CLOSED_PERMANENTLY places -- merge_records previously always marked
    every new institution OPERATIONAL regardless, letting a closed business
    appear active and proceed into qualification or outreach. Other source
    types have no equivalent signal yet, so they default to UNKNOWN rather
    than guessing OPERATIONAL for them.
    """
    if record.source_type == SourceType.GOOGLE_PLACES:
        payload = record.raw_payload or {}
        return _GOOGLE_BUSINESS_STATUS_MAP.get(
            payload.get("businessStatus"), OperatingStatus.UNKNOWN
        )
    return OperatingStatus.UNKNOWN


def display_fields(record: RawSourceRecord) -> dict[str, Any]:
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
        # The raw display name (original casing/punctuation, e.g. "St.
        # Mary's School") is what institution APIs/the UI should show --
        # normalized_name exists purely for blocking/scoring's exact-string
        # comparisons and is always populated for a live record, so
        # preferring it here would always win and silently present every
        # Google Places institution's name lowercased and punctuation-
        # stripped, unlike manually entered institutions.
        name = payload.get("displayName", {}).get("text") or record.normalized_name or "Unknown"
        return {
            "name": name,
            "address": payload.get("formattedAddress", ""),
            "website": payload.get("websiteUri"),
            "email": None,
            "institution_type": payload.get("primaryType", ""),
            "city": "",
            "country_code": "",
        }

    if record.source_type == SourceType.WEBSITE:
        # Same reasoning as the Google Places branch above: normalized_name
        # is always populated by _run_web_crawler() and would otherwise
        # always win, silently presenting every crawled institution's name
        # lowercased and punctuation-stripped. Prefer the raw "organization"
        # (or "name") value from raw_payload for presentation instead.
        name = (
            payload.get("organization")
            or payload.get("name")
            or record.normalized_name
            or "Unknown"
        )
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
            "city": "",
            "country_code": "",
        }

    if record.source_type == SourceType.MANUAL:
        # Same reasoning as the Google Places/WEBSITE branches above:
        # normalized_name is always populated for manual entries too, so it
        # would otherwise always win and discard the user-entered casing --
        # showing the resolution queue's matching key instead of what the
        # user actually typed when a later scraped record is compared
        # against this one.
        name = payload.get("institution_name") or record.normalized_name or "Unknown"
        return {
            "name": name,
            "address": payload.get("address", ""),
            "website": payload.get("website"),
            "email": None,
            "institution_type": payload.get("institution_type", ""),
            "city": "",
            "country_code": "",
        }

    if record.source_type == SourceType.AUTHORIZED_IMPORT:
        # Same reasoning as the MANUAL branch above: normalized_name is
        # always populated by parse_authorized_import_csv/_run_authorized_import
        # too, so it would otherwise always win and discard the
        # spreadsheet's original casing/punctuation.
        name = payload.get("institution_name") or record.normalized_name or "Unknown"
        contacts = payload.get("contacts") or []
        email = next(
            (c["contact_value"] for c in contacts if c.get("contact_type") == "email"), None
        )
        return {
            "name": name,
            "address": payload.get("address", ""),
            "website": payload.get("website") or None,
            "email": email,
            "institution_type": payload.get("institution_type", ""),
            "city": payload.get("city", ""),
            "country_code": payload.get("country_code", ""),
            # Every contact this institution declared (any contact_type,
            # with person_name/role) -- see _add_contacts_and_provenance,
            # which writes all of them instead of just the single "email"
            # key above (kept for callers that only need the one field).
            "declared_contacts": contacts,
        }

    if record.source_type == SourceType.YANDEX:
        # sources/yandex_maps.py's raw_payload is the connector's raw
        # GeoJSON Feature, unpacked here the same way the GOOGLE_PLACES
        # branch above unpacks its raw Places API response.
        properties = payload.get("properties", {})
        company = properties.get("CompanyMetaData", {})
        name = company.get("name") or properties.get("name") or record.normalized_name or "Unknown"
        categories = company.get("Categories") or []
        return {
            "name": name,
            "address": company.get("address") or properties.get("description", ""),
            "website": company.get("url") or None,
            "email": None,
            "institution_type": categories[0].get("name", "") if categories else "",
            "city": "",
            "country_code": "",
        }

    if record.source_type == SourceType.APPLE_MAPS:
        # Apple's /v1/search response has no email/institution_type/city/
        # country_code fields at all (see sources/apple_maps.py's own
        # known-v1-limitation docstring note) -- left blank/None here
        # rather than guessed, same as the GOOGLE_PLACES branch already
        # does when a field genuinely isn't in the source payload.
        name = payload.get("name") or record.normalized_name or "Unknown"
        address_lines = payload.get("formattedAddressLines") or []
        return {
            "name": name,
            "address": ", ".join(address_lines),
            "website": None,
            "email": None,
            "institution_type": "",
            "city": "",
            "country_code": "",
        }

    if record.source_type == SourceType.TELEGRAM:
        # sources/telegram_channels.py's raw_payload is its own fetch_channel
        # dict (name/description/all_emails/all_phones), not a third-party
        # API response shape.
        name = payload.get("name") or record.normalized_name or "Unknown"
        emails = payload.get("all_emails") or []
        return {
            "name": name,
            "address": "",
            "website": None,
            "email": emails[0] if emails else None,
            "institution_type": "",
            "city": "",
            "country_code": "",
        }

    # No connector exists yet for LINKEDIN -- its raw records never reach
    # display_fields in practice (see the _RESOLUTION_ELIGIBLE_SOURCE_TYPES
    # comment in pipeline.py: LINKEDIN goes through
    # intelligence/researcher.py's AI-driven path instead of
    # resolve_incoming_record), but this fallback stays as a safety net
    # rather than guessing at an unknown raw_payload shape.
    return {
        "name": record.normalized_name or "Unknown",
        "address": "",
        "website": record.normalized_domain,
        "email": None,
        "institution_type": "",
        "city": "",
        "country_code": "",
    }


def _provider_ids_list(provider_ids: dict, source_type: str) -> list[str]:
    """
    Reads a provider_ids entry as a list regardless of whether it was
    written in the current list-per-source_type shape or the legacy
    scalar-per-source_type shape (a single source_id string, predating
    _provider_ids_for). `list("some-id-string")` would silently shatter a
    legacy scalar into one list entry per character -- guard against that
    by wrapping a bare str as a single-element list instead of iterating it.
    """
    value = provider_ids.get(source_type, [])
    if isinstance(value, str):
        return [value]
    return list(value)


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


def _synthesize_branch_fields(records: list[RawSourceRecord]) -> dict:
    """
    address/location previously came only from records[0] -- fine for the
    single-record case (_create_branches' same_location=False path, and
    attach_record_to_institution's "Additional Campus" path, both always
    call this with a one-element list), but same_location=True collapses
    the ENTIRE merge group into one shared Branch, and records[0] there is
    just whichever record _apply_decision happened to pass first. If that
    record is sparse (e.g. a website-crawled lead with no location) while
    another record in the same group has better data (e.g. the matched
    Places record's formattedAddress/location), that evidence was silently
    dropped even though same_location=True means they all describe the
    exact same physical location. First non-empty value wins, in record
    order -- same policy as _synthesize_institution_fields.
    """
    address = None
    location = None
    city = None
    country_code = None
    for r in records:
        fields = display_fields(r)
        if not address and fields["address"]:
            address = fields["address"]
        if location is None and r.location is not None:
            location = r.location
        # city/country_code: same first-non-empty-wins policy. Only
        # AUTHORIZED_IMPORT supplies real values today (Google Places'
        # response has no structured address components, and the web
        # crawler/manual paths have no equivalent field) -- every other
        # source's display_fields returns "" for both, so this falls
        # through to _build_branch's UNKNOWN sentinel unchanged for them.
        if not city and fields.get("city"):
            city = fields["city"]
        if not country_code and fields.get("country_code"):
            country_code = fields["country_code"]
    return {"address": address, "location": location, "city": city, "country_code": country_code}


def _build_branch(
    records: list[RawSourceRecord], institution_id: uuid.UUID, *, branch_name: str
) -> Branch:
    synthesized = _synthesize_branch_fields(records)
    return Branch(
        institution_id=institution_id,
        branch_name=branch_name,
        address=synthesized["address"] or "",
        city=synthesized["city"] or _UNKNOWN_CITY,
        country_code=synthesized["country_code"] or _UNKNOWN_COUNTRY_CODE,
        location=synthesized["location"],
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

    fields = display_fields(record)
    declared_contacts = fields.get("declared_contacts")
    if declared_contacts is not None:
        # This source declares its own explicit contact list (currently
        # only AUTHORIZED_IMPORT, where a CSV row's contact_type is
        # arbitrary -- phone, email, whatsapp, telegram, other). Writing
        # only phone (from normalized_phone) + email (from the "email" key
        # below) silently dropped every other contact_type entirely, and
        # dropped person_name/role even for phone/email rows. Write every
        # declared contact instead, with whatever type/person_name/role it
        # actually carries.
        for contact in declared_contacts:
            contact_type = contact["contact_type"]
            contact_value = contact["contact_value"]
            if contact_type == "phone":
                # Store the same normalized E.164 form record.normalized_phone
                # already uses for blocking, not the raw CSV value -- a
                # phone entered in national/formatted form ("0300
                # 1234567") and a later Places/manual record for the same
                # institution storing "+923001234567" would otherwise be
                # treated as two distinct contact_values by
                # _find_contact_point's exact match, creating a duplicate
                # ContactPoint for the same physical number.
                contact_value = normalize_phone(
                    contact_value, default_region=fields.get("country_code") or None
                )
            await _add_contact_if_present(
                session,
                institution,
                record,
                contact_type=contact_type,
                contact_value=contact_value,
                person_name=contact.get("person_name") or None,
                role=contact.get("role") or None,
            )
        return

    await _add_contact_if_present(
        session, institution, record, contact_type="phone", contact_value=record.normalized_phone
    )
    await _add_contact_if_present(
        session, institution, record, contact_type="email", contact_value=fields.get("email")
    )


async def _add_contact_if_present(
    session: AsyncSession,
    institution: CanonicalInstitution,
    record: RawSourceRecord,
    *,
    contact_type: str,
    contact_value: str | None,
    person_name: str | None = None,
    role: str | None = None,
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
        candidate = await resolve_person_candidate(session, institution.id, person_name)
        session.add(
            ContactPoint(
                institution_id=institution.id,
                contact_type=contact_type,
                contact_value=contact_value,
                person_name=person_name,
                role=role,
                person_candidate_id=candidate.id if candidate else None,
            )
        )
    else:
        # A later import/rediscovery can supply (or correct) the
        # decision-maker metadata for a contact whose type+value were
        # already known -- update rather than silently leaving the
        # existing row's person_name/role stale forever (only ever
        # written here on first creation, previously).
        if person_name and existing.person_name != person_name:
            existing.person_name = person_name
            candidate = await resolve_person_candidate(session, institution.id, person_name)
            existing.person_candidate_id = candidate.id if candidate else None
        if role and existing.role != role:
            existing.role = role
    session.add(
        FieldProvenance(
            canonical_id=institution.id,
            raw_record_id=record.id,
            field_name=f"contact_{contact_type}",
            asserted_value=contact_value,
            assertion_trust=1.0,
        )
    )


def _aggregate_institution_status(statuses: list[OperatingStatus]) -> OperatingStatus:
    """
    Combines every raw record's operating status into a single
    institution-level status. merge_records groups records describing
    DISTINCT physical branches just as often as it groups records
    describing the same location (same_location=False is the default,
    used whenever a reviewer creates separate branches for a multi-campus
    institution) -- picking whichever record's non-UNKNOWN status came
    first in raw_records order previously promoted one arbitrary campus's
    status to represent the whole institution, so a closed incoming
    campus could mark an otherwise-thriving multi-branch institution
    closed, while an operational first campus could conceal a closed
    sibling entirely. An institution with at least one OPERATIONAL branch
    is still a live lead overall (reach out to that branch specifically);
    it's only CLOSED_PERMANENTLY once every branch that reported a status
    agrees, and CLOSED_TEMPORARILY is treated as the more optimistic
    reading of a permanent/temporary mix since a temporary closure can
    still reopen.
    """
    non_unknown = [s for s in statuses if s != OperatingStatus.UNKNOWN]
    if not non_unknown:
        return OperatingStatus.UNKNOWN
    if OperatingStatus.OPERATIONAL in non_unknown:
        return OperatingStatus.OPERATIONAL
    if OperatingStatus.CLOSED_TEMPORARILY in non_unknown:
        return OperatingStatus.CLOSED_TEMPORARILY
    return OperatingStatus.CLOSED_PERMANENTLY


def _synthesize_institution_fields(raw_records: list[RawSourceRecord]) -> dict:
    """
    website/domain/institution_type/status previously came only from
    raw_records[0] (the incoming record, since _apply_decision always
    passes it first) -- if that record is sparse (e.g. a website-crawled
    lead with no domain/status) while another record in the same merge
    group supplies them (e.g. the matched Places record's website and
    businessStatus), that evidence was silently dropped even though it's
    right there in the merge group, leaving a null domain/UNKNOWN status on
    the resulting institution despite the raw ledger having the answer.
    First non-empty value wins, in record order, for website/domain/
    institution_type -- canonical_name is deliberately NOT synthesized
    this way (kept from the primary record only), since picking a "best"
    display name across sources is a separate, more subjective concern
    than backfilling a missing field. status is synthesized differently
    (see _aggregate_institution_status): first-non-empty-wins is wrong for
    a per-location fact that can span multiple distinct branches.
    """
    website = None
    domain = None
    institution_type = ""
    statuses = []
    for r in raw_records:
        fields = display_fields(r)
        if not website and fields["website"]:
            website = fields["website"]
        if not domain and r.normalized_domain:
            domain = r.normalized_domain
        if not institution_type and fields["institution_type"]:
            institution_type = fields["institution_type"]
        statuses.append(_operating_status(r))
    return {
        "website": website,
        "domain": domain,
        "institution_type": institution_type,
        "status": _aggregate_institution_status(statuses),
    }


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
    synthesized = _synthesize_institution_fields(raw_records)

    institution = CanonicalInstitution(
        canonical_name=fields["name"],
        institution_type=synthesized["institution_type"],
        domain=synthesized["domain"],
        website=synthesized["website"],
        status=synthesized["status"],
        confidence_score=confidence_for_source_count(len(raw_records)),
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
        if record.source_id in _provider_ids_list(branch.provider_ids, record.source_type.value):
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
    # Two concurrent calls attaching different incoming records to the same
    # institution/branch (e.g. two reviewer decisions targeting the same
    # branch, or two overlapping ingestion runs) would otherwise both read
    # the same provider_ids/confidence_score snapshot and the later commit
    # silently overwrites the earlier one's update -- a lost source ID (see
    # find_branch_for_raw_record) or a lost +10 confidence_score increment.
    # Locking (and, since the row may already be identity-mapped from an
    # earlier query in this same session, refreshing) institution first and
    # then target_branch -- a fixed order, to avoid deadlocking against a
    # concurrent transaction locking the same two rows -- makes the second
    # transaction block until the first commits, and then actually see its
    # committed values rather than a stale in-memory snapshot.
    await session.refresh(institution, with_for_update=True)
    if target_branch is not None:
        await session.refresh(target_branch, with_for_update=True)

    fields = display_fields(record)
    # The first record to form an institution may lack a website/domain
    # (e.g. a Google Places result with no listed site); a later same-
    # institution match that does supply one was previously only ever
    # stored in the raw ledger (raw_payload/FieldProvenance) and never
    # backfilled onto the canonical row itself, leaving dossiers and other
    # downstream consumers reading institution.website/domain permanently
    # incomplete despite the evidence already being on hand.
    if not institution.website and fields["website"]:
        institution.website = fields["website"]
    if not institution.domain and record.normalized_domain:
        institution.domain = record.normalized_domain
    if not institution.institution_type and fields["institution_type"]:
        institution.institution_type = fields["institution_type"]

    if target_branch is not None:
        # Operating status is per-location evidence -- only trust it as the
        # institution's overall status when this record describes the SAME
        # branch/location the institution's status is presumably already
        # tracking (target_branch is not None). target_branch=None means a
        # DISTINCT new branch (a multi-campus institution): that branch's
        # own closure (or a newly-added branch being active) must not
        # overwrite the whole institution's status one way or the other --
        # unlike website/domain (fill-if-missing, since those don't change
        # once known), operating status is a point-in-time fact that a
        # rediscovery can genuinely update in either direction (closed
        # permanently, or reopened), so this always trusts the newest
        # same-branch record's asserted status.
        #
        # But that trust only extends as far as this record's own branch --
        # Branch has no per-branch status column, so once an institution has
        # more than one branch there's no way to re-derive the institution-
        # wide status from every branch's latest known state the way
        # _aggregate_institution_status does at creation time. Applying this
        # one branch's status directly to the whole institution would
        # silently mark every other still-operational campus closed just
        # because one of them reported closure. OPERATIONAL is always safe
        # to apply regardless of branch count (an institution with at least
        # one confirmed-active branch is still a live lead overall, matching
        # _aggregate_institution_status's own "OPERATIONAL wins" policy);
        # a closure is only applied directly when this is the institution's
        # only branch, where branch-level and institution-level status are
        # the same fact.
        new_status = _operating_status(record)
        if new_status == OperatingStatus.OPERATIONAL:
            institution.status = new_status
        elif new_status != OperatingStatus.UNKNOWN:
            branch_count = await session.scalar(
                select(func.count())
                .select_from(Branch)
                .where(Branch.institution_id == institution.id)
            )
            if branch_count <= 1:
                institution.status = new_status

        if not target_branch.address and fields["address"]:
            target_branch.address = fields["address"]
        # city/country_code are NOT NULL, so a branch created without real
        # values always holds the UNKNOWN sentinels rather than being
        # blank -- backfill only replaces those sentinels, the same
        # fill-if-missing policy as address above.
        if target_branch.city == _UNKNOWN_CITY and fields.get("city"):
            target_branch.city = fields["city"]
        if target_branch.country_code == _UNKNOWN_COUNTRY_CODE and fields.get("country_code"):
            target_branch.country_code = fields["country_code"]
        # provider_ids is a plain JSONB column (no MutableDict tracking), so
        # mutating the existing dict/list in place would never be detected
        # as a change -- reassign a new dict (with a new list for this
        # source_type) so the attribute-set event actually marks the branch
        # dirty. Appending to the list (not overwriting the key) so this
        # doesn't lose a previously-recorded source_id for the same
        # source_type -- see _provider_ids_for's docstring. Read via
        # _provider_ids_list rather than a bare list(...) coercion so a
        # legacy scalar value under this key doesn't get shattered into one
        # list entry per character.
        source_type = record.source_type.value
        existing_ids = _provider_ids_list(target_branch.provider_ids, source_type)
        # A repeated ingestion of the exact same provider record (e.g. a
        # rerun scrape returning the identical Google Place) contributes no
        # new independent evidence -- only bump confidence_score below when
        # this source_id is genuinely new to the branch.
        is_new_evidence = record.source_id not in existing_ids
        if is_new_evidence:
            existing_ids.append(record.source_id)
            target_branch.provider_ids = {**target_branch.provider_ids, source_type: existing_ids}
        branch = target_branch
    else:
        is_new_evidence = True
        branch = _build_branch([record], institution.id, branch_name="Additional Campus")
        session.add(branch)

    await _add_contacts_and_provenance(session, institution, record)
    if is_new_evidence:
        institution.confidence_score = bump_confidence(institution.confidence_score)

    return branch
