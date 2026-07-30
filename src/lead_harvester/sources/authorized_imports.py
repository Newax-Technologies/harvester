"""
Authorized Imports Connector
============================
Parses a CSV of licensed or manually-sourced institution + contact data into
normalized records for the resolution pipeline -- the accepted alternative
to unauthorized scraping/account automation for a source with no live API
(docs/ROADMAP.md's Module #2: "Unauthorized scraping/account automation is
out of bounds; authorized imports and licensed/manual research are the
accepted pattern").

One CSV row = one institution + one contact, using the same flattened field
shape as the manual-lead API (ManualLeadIn):
  institution_name (required), institution_type, website, address, city,
  country, country_code, contact_type, contact_value (required), person_name,
  role, notes

A malformed or blank row (missing institution_name/contact_value, or a row
that raises while parsing) is skipped and logged rather than aborting the
whole batch -- one bad line in a hand-edited spreadsheet must not discard
every other row in it, matching pipeline.py's own per-record isolation
convention (_resolve_or_log).
"""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass


@dataclass(slots=True)
class AuthorizedImportRecord:
    institution_name: str
    institution_type: str
    website: str
    address: str
    city: str
    country: str
    country_code: str
    contact_type: str
    contact_value: str
    person_name: str
    role: str
    notes: str
    # Identifies the license/agreement or manual-research source this row
    # came from, for compliance traceability -- distinct from per-row notes,
    # and always the same value for every row in one import run (passed in
    # by the caller, not read from the CSV itself).
    source_reference: str


@dataclass(slots=True)
class AuthorizedImportResult:
    records: list[AuthorizedImportRecord]
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
    Parses CSV text (one row = one institution + one contact) into
    normalized AuthorizedImportRecord entries. Raises ValueError up front if
    the header row is missing either required column -- that's a structural
    problem with the whole file, not a single bad row, so it isn't worth
    skip-and-continue treatment. Individual data rows missing a required
    value, or that otherwise fail to parse, are skipped and collected into
    `skipped` instead of raising.
    """
    reader = csv.DictReader(io.StringIO(text))
    header = set(reader.fieldnames or [])
    missing = _REQUIRED_COLUMNS - header
    if missing:
        raise ValueError(f"CSV is missing required column(s): {', '.join(sorted(missing))}")

    records: list[AuthorizedImportRecord] = []
    skipped: list[str] = []

    for row_number, row in enumerate(reader, start=1):
        try:
            record = _parse_row(
                row,
                source_reference=source_reference,
                default_country_code=default_country_code,
                default_country=default_country,
            )
        except ValueError as e:
            skipped.append(f"row {row_number}: {e}")
            continue
        records.append(record)

    return AuthorizedImportResult(records=records, skipped=skipped)


def _parse_row(
    row: dict[str, str | None],
    *,
    source_reference: str,
    default_country_code: str,
    default_country: str,
) -> AuthorizedImportRecord:
    institution_name = (row.get("institution_name") or "").strip()
    if not institution_name:
        raise ValueError("institution_name is required")

    contact_value = (row.get("contact_value") or "").strip()
    if not contact_value:
        raise ValueError("contact_value is required")

    country_code = (row.get("country_code") or "").strip().upper() or default_country_code
    if len(country_code) != 2 or not country_code.isalpha():
        raise ValueError(f"country_code must be two letters, got {country_code!r}")

    return AuthorizedImportRecord(
        institution_name=institution_name,
        institution_type=(row.get("institution_type") or "").strip() or "school",
        website=(row.get("website") or "").strip(),
        address=(row.get("address") or "").strip(),
        city=(row.get("city") or "").strip(),
        country=(row.get("country") or "").strip() or default_country,
        country_code=country_code,
        contact_type=(row.get("contact_type") or "").strip().lower() or "phone",
        contact_value=contact_value,
        person_name=(row.get("person_name") or "").strip(),
        role=(row.get("role") or "").strip(),
        notes=(row.get("notes") or "").strip(),
        source_reference=source_reference,
    )
