"""
Authorized Imports Connector
============================
Parses a CSV of licensed or manually-sourced institution + contact data into
normalized records for the resolution pipeline -- the accepted alternative
to unauthorized scraping/account automation for a source with no live API
(docs/ROADMAP.md's Module #2: "Unauthorized scraping/account automation is
out of bounds; authorized imports and licensed/manual research are the
accepted pattern").

Each CSV row declares one institution + one contact, using the same
flattened field shape as the manual-lead API (ManualLeadIn):
  institution_name (required), institution_type, website, address, city,
  country, country_code, contact_type, contact_value (required), person_name,
  role, notes

Rows are GROUPED by institution identity (normalized name + website domain,
falling back to normalized address when there's no website) into one
AuthorizedImportInstitution per institution, carrying every declared
contact -- not one RawSourceRecord per row. Without this, a school listed
across two rows (e.g. a phone contact and an email contact) produced two
independent raw records that the resolution pipeline's blocking strategies
(phone/domain/geography -- see resolution/blocking.py) have no way to link
back together, since neither row alone carries a phone+geo or domain match:
each row silently became its own separate canonical institution instead of
one institution with two contacts.

A malformed or blank row (missing institution_name/contact_value, or a row
that raises while parsing) is skipped and logged rather than aborting the
whole batch -- one bad line in a hand-edited spreadsheet must not discard
every other row in it, matching pipeline.py's own per-record isolation
convention (_resolve_or_log).
"""

from __future__ import annotations

import csv
import hashlib
import io
from dataclasses import dataclass, field

from ..resolution.normalize import (
    country_to_iso2,
    normalize_address,
    normalize_domain,
    normalize_name,
)


@dataclass(slots=True)
class AuthorizedImportContact:
    contact_type: str
    contact_value: str
    person_name: str
    role: str


@dataclass(slots=True)
class AuthorizedImportInstitution:
    institution_name: str
    institution_type: str
    website: str
    address: str
    city: str
    country: str
    country_code: str
    notes: str
    # Identifies the license/agreement or manual-research source this
    # institution came from, for compliance traceability -- distinct from
    # per-row notes, and always the same value for every institution in one
    # import run (passed in by the caller, not read from the CSV itself).
    source_reference: str
    contacts: list[AuthorizedImportContact] = field(default_factory=list)
    # The exact signal (website domain, normalized address, city, or a
    # per-row fallback) that established this institution's identity for
    # GROUPING -- see the key_suffix computation in
    # parse_authorized_import_csv. Fixed once, by whichever row first
    # created this group; source_id derives from this instead of
    # recomputing from self.website/self.address, since those fields can be
    # backfilled by a LATER row after grouping already happened (first-
    # non-empty-wins) without changing which signal actually distinguished
    # this institution from a same-named one grouped differently.
    identity_key_suffix: str = ""

    @property
    def source_id(self) -> str:
        """
        A stable identity for this institution within this source_reference,
        derived from its own normalized name + identity_key_suffix rather
        than the row's ordinal position in the file. An ordinal shifts if
        the spreadsheet is reordered or gains a row -- an unchanged
        institution would receive a new ID, and Branch.provider_ids/
        find_branch_for_raw_record treat source_type+source_id as the
        identity of an exact physical location, so a reordered rerun could
        enrich the wrong branch or be counted as new independent evidence.
        Re-importing the same institution (even from a re-ordered or
        appended-to file) now produces the same source_id.

        Deliberately uses identity_key_suffix (the signal that actually
        distinguished this institution during grouping) rather than
        recomputing from self.website/self.address: without this, two
        same-named institutions with neither a website nor an address (in
        different cities, or two otherwise-bare rows) were correctly split
        into separate AuthorizedImportInstitution objects by the grouping
        key, but both computed the SAME digest here (address always empty
        for both) -- _find_authorized_import_record then treated the
        second as an update of the first, silently skipping it or
        attaching its contacts to the wrong canonical institution.
        """
        digest = hashlib.sha256(
            f"{normalize_name(self.institution_name)}|{self.identity_key_suffix}".encode()
        ).hexdigest()[:16]
        return f"{self.source_reference}:{digest}"


@dataclass(slots=True)
class AuthorizedImportResult:
    institutions: list[AuthorizedImportInstitution]
    # One entry per skipped row: "row <n>: <reason>", 1-indexed against the
    # data rows (excluding the header), so a caller can point a human back
    # at the exact line to fix in the original file.
    skipped: list[str]


_REQUIRED_COLUMNS = {"institution_name", "contact_value"}


def parse_authorized_import_csv(
    text: str,
    *,
    source_reference: str,
    default_country_code: str = "PK",
    default_country: str = "Pakistan",
) -> AuthorizedImportResult:
    """
    Parses CSV text into normalized AuthorizedImportInstitution entries,
    one per distinct institution (grouping rows that describe the same
    institution -- see AuthorizedImportInstitution's docstring). Raises
    ValueError up front if the header row is missing either required
    column -- that's a structural problem with the whole file, not a
    single bad row, so it isn't worth skip-and-continue treatment.
    Individual data rows missing a required value, or that otherwise fail
    to parse, are skipped and collected into `skipped` instead of raising.
    """
    reader = csv.DictReader(io.StringIO(text))
    header = set(reader.fieldnames or [])
    missing = _REQUIRED_COLUMNS - header
    if missing:
        raise ValueError(f"CSV is missing required column(s): {', '.join(sorted(missing))}")

    skipped: list[str] = []
    groups: dict[tuple[str, str], AuthorizedImportInstitution] = {}
    order: list[tuple[str, str]] = []

    for row_number, row in enumerate(reader, start=1):
        try:
            institution_fields, contact = _parse_row(
                row,
                default_country_code=default_country_code,
                default_country=default_country,
            )
        except ValueError as e:
            skipped.append(f"row {row_number}: {e}")
            continue

        if institution_fields["website"]:
            key_suffix = normalize_domain(institution_fields["website"])
        elif institution_fields["address"]:
            key_suffix = normalize_address(institution_fields["address"])
        elif institution_fields["city"]:
            # No website or address, but a city is still a real
            # distinguishing signal -- e.g. two rows for the same
            # institution (a phone-only row and an email-only row) neither
            # of which happens to list an address. Falls through to the
            # row-number branch below only when even this is missing.
            key_suffix = f"city:{institution_fields['city'].strip().lower()}"
        else:
            # Nothing distinguishes this institution from another row with
            # the same name at all -- every such row previously grouped
            # under the same (name, "") key, silently collapsing two
            # genuinely distinct institutions (e.g. same-named campuses in
            # different, unrecorded cities) into one: the later row's
            # location/contacts overwrote the first's, and both rows'
            # contacts landed on a single canonical entity. A bare row like
            # this can't safely be grouped with anything -- key it by its
            # own row number so it always gets its own institution instead
            # of gambling on a name-only match.
            key_suffix = f"row:{row_number}"
        key = (normalize_name(institution_fields["institution_name"]), key_suffix)
        existing = groups.get(key)
        if existing is None:
            existing = AuthorizedImportInstitution(
                **institution_fields,
                source_reference=source_reference,
                identity_key_suffix=key_suffix,
            )
            groups[key] = existing
            order.append(key)
        else:
            # First non-empty value wins for institution-level fields, in
            # row order -- a later row for the same institution may supply
            # a field an earlier row left blank.
            for attr in (
                "institution_type",
                "website",
                "address",
                "city",
                "country",
                "country_code",
                "notes",
            ):
                if not getattr(existing, attr) and institution_fields[attr]:
                    setattr(existing, attr, institution_fields[attr])

        # Skip an exact duplicate contact (same type+value) already
        # recorded for this institution, e.g. the same row appearing twice.
        if not any(
            c.contact_type == contact.contact_type and c.contact_value == contact.contact_value
            for c in existing.contacts
        ):
            existing.contacts.append(contact)

    institutions = [groups[key] for key in order]
    return AuthorizedImportResult(institutions=institutions, skipped=skipped)


def _parse_row(
    row: dict[str, str | None],
    *,
    default_country_code: str,
    default_country: str,
) -> tuple[dict[str, str], AuthorizedImportContact]:
    institution_name = (row.get("institution_name") or "").strip()
    if not institution_name:
        raise ValueError("institution_name is required")

    contact_value = (row.get("contact_value") or "").strip()
    if not contact_value:
        raise ValueError("contact_value is required")

    # An explicit country_code column always wins. Otherwise, derive it
    # from the free-text country column (e.g. "United Arab Emirates")
    # rather than blindly falling back to default_country_code regardless
    # of what country the row actually names -- previously a UAE row with
    # no country_code column silently got tagged with whatever the
    # pipeline's default happened to be (e.g. "PK").
    raw_country_code = (row.get("country_code") or "").strip().upper()
    country_code = (
        raw_country_code
        or country_to_iso2((row.get("country") or "").strip())
        or default_country_code
    )
    if len(country_code) != 2 or not country_code.isalpha():
        raise ValueError(f"country_code must be two letters, got {country_code!r}")

    institution_fields = {
        "institution_name": institution_name,
        "institution_type": (row.get("institution_type") or "").strip() or "school",
        "website": (row.get("website") or "").strip(),
        "address": (row.get("address") or "").strip(),
        "city": (row.get("city") or "").strip(),
        "country": (row.get("country") or "").strip() or default_country,
        "country_code": country_code,
        "notes": (row.get("notes") or "").strip(),
    }
    contact = AuthorizedImportContact(
        contact_type=(row.get("contact_type") or "").strip().lower() or "phone",
        contact_value=contact_value,
        person_name=(row.get("person_name") or "").strip(),
        role=(row.get("role") or "").strip(),
    )
    return institution_fields, contact
