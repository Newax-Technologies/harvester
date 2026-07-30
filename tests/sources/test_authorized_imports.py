import pytest

from lead_harvester.sources.authorized_imports import parse_authorized_import_csv


def test_parses_valid_rows():
    csv_text = (
        "institution_name,institution_type,website,address,city,country,country_code,"
        "contact_type,contact_value,person_name,role,notes\n"
        "Beacon House School,school,https://beaconhouse.example.edu,"
        "Plot 12 Block B,Karachi,Pakistan,PK,phone,+923001234567,Ali Khan,Principal,Referral\n"
        "Riverside Academy,,,,,,,email,admissions@riverside.example.edu,,,\n"
    )

    result = parse_authorized_import_csv(
        csv_text, source_reference="license-2026-education-directory"
    )

    assert result.skipped == []
    assert len(result.records) == 2

    first = result.records[0]
    assert first.institution_name == "Beacon House School"
    assert first.institution_type == "school"
    assert first.website == "https://beaconhouse.example.edu"
    assert first.city == "Karachi"
    assert first.country_code == "PK"
    assert first.contact_type == "phone"
    assert first.contact_value == "+923001234567"
    assert first.person_name == "Ali Khan"
    assert first.source_reference == "license-2026-education-directory"

    second = result.records[1]
    # Blank optional columns fall back to sensible defaults, not blanks.
    assert second.institution_type == "school"
    assert second.country_code == "PK"
    assert second.contact_type == "email"
    assert second.contact_value == "admissions@riverside.example.edu"


def test_raises_on_missing_required_column():
    csv_text = "institution_name,website\nBeacon House School,https://example.edu\n"

    with pytest.raises(ValueError, match="contact_value"):
        parse_authorized_import_csv(csv_text, source_reference="license-2026")


def test_skips_blank_or_malformed_rows_without_aborting_the_batch():
    csv_text = (
        "institution_name,contact_value,country_code\n"
        "Good School,+923001234567,PK\n"
        ",+923009999999,PK\n"  # missing institution_name
        "Another School,,PK\n"  # missing contact_value
        "Bad Country School,+923005555555,USA\n"  # not a 2-letter code
        "Second Good School,admissions@example.edu,PK\n"
    )

    result = parse_authorized_import_csv(csv_text, source_reference="license-2026")

    assert [r.institution_name for r in result.records] == ["Good School", "Second Good School"]
    assert len(result.skipped) == 3
    assert "row 2" in result.skipped[0]
    assert "row 3" in result.skipped[1]
    assert "row 4" in result.skipped[2]


def test_default_country_code_applied_when_column_blank():
    csv_text = "institution_name,contact_value\nSchool A,+923001234567\n"

    result = parse_authorized_import_csv(
        csv_text, source_reference="license-2026", default_country_code="AE"
    )

    assert result.records[0].country_code == "AE"
