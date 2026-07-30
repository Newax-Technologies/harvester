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
    assert len(result.institutions) == 2

    first = result.institutions[0]
    assert first.institution_name == "Beacon House School"
    assert first.institution_type == "school"
    assert first.website == "https://beaconhouse.example.edu"
    assert first.city == "Karachi"
    assert first.country_code == "PK"
    assert first.source_reference == "license-2026-education-directory"
    assert len(first.contacts) == 1
    assert first.contacts[0].contact_type == "phone"
    assert first.contacts[0].contact_value == "+923001234567"
    assert first.contacts[0].person_name == "Ali Khan"

    second = result.institutions[1]
    # Blank optional columns fall back to sensible defaults, not blanks.
    assert second.institution_type == "school"
    assert second.country_code == "PK"
    assert second.contacts[0].contact_type == "email"
    assert second.contacts[0].contact_value == "admissions@riverside.example.edu"


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

    assert [i.institution_name for i in result.institutions] == [
        "Good School",
        "Second Good School",
    ]
    assert len(result.skipped) == 3
    assert "row 2" in result.skipped[0]
    assert "row 3" in result.skipped[1]
    assert "row 4" in result.skipped[2]


def test_default_country_code_applied_when_column_blank():
    csv_text = "institution_name,contact_value\nSchool A,+923001234567\n"

    result = parse_authorized_import_csv(
        csv_text, source_reference="license-2026", default_country_code="AE"
    )

    assert result.institutions[0].country_code == "AE"


def test_groups_rows_sharing_institution_identity_into_one_institution():
    # Two rows describing the same school (matched by normalized name +
    # website) previously became two independent RawSourceRecords that the
    # resolution pipeline's blocking strategies (phone/domain/geography)
    # have no way to link back together, since neither row alone carries a
    # phone+geo or domain match -- each silently became its own separate
    # canonical institution. Grouping at parse time means both contacts
    # end up on the SAME institution before resolution ever runs.
    csv_text = (
        "institution_name,website,address,city,country_code,contact_type,contact_value,"
        "person_name,role\n"
        "Beacon House School,https://beaconhouse.example.edu,,,PK,phone,+923001234567,"
        "Ali Khan,Principal\n"
        "beacon house school,https://beaconhouse.example.edu,Plot 12 Block B,Karachi,PK,"
        "email,admissions@beaconhouse.example.edu,,\n"
    )

    result = parse_authorized_import_csv(csv_text, source_reference="license-2026")

    assert len(result.institutions) == 1
    institution = result.institutions[0]
    assert len(institution.contacts) == 2
    assert {c.contact_type for c in institution.contacts} == {"phone", "email"}
    # First-non-empty-wins fill-in from the second row for fields the
    # first row left blank.
    assert institution.address == "Plot 12 Block B"
    assert institution.city == "Karachi"


def test_groups_by_normalized_address_when_no_website():
    csv_text = (
        "institution_name,address,contact_type,contact_value\n"
        "Riverside Academy,12 River Road Karachi,phone,+923001234567\n"
        "Riverside Academy,12 River Road Karachi,email,admissions@example.edu\n"
    )

    result = parse_authorized_import_csv(csv_text, source_reference="license-2026")

    assert len(result.institutions) == 1
    assert len(result.institutions[0].contacts) == 2


def test_distinct_institutions_with_same_name_different_address_stay_separate():
    csv_text = (
        "institution_name,address,contact_type,contact_value\n"
        "Riverside Academy,Karachi Campus,phone,+923001111111\n"
        "Riverside Academy,Lahore Campus,phone,+923002222222\n"
    )

    result = parse_authorized_import_csv(csv_text, source_reference="license-2026")

    assert len(result.institutions) == 2


def test_source_id_is_stable_regardless_of_row_order():
    csv_a = (
        "institution_name,website,contact_type,contact_value\n"
        "Beacon House School,https://beaconhouse.example.edu,phone,+923001234567\n"
        "Riverside Academy,https://riverside.example.edu,email,admissions@riverside.example.edu\n"
    )
    csv_b = (
        "institution_name,website,contact_type,contact_value\n"
        "Riverside Academy,https://riverside.example.edu,email,admissions@riverside.example.edu\n"
        "Beacon House School,https://beaconhouse.example.edu,phone,+923001234567\n"
    )

    result_a = parse_authorized_import_csv(csv_a, source_reference="license-2026")
    result_b = parse_authorized_import_csv(csv_b, source_reference="license-2026")

    ids_a = {i.institution_name: i.source_id for i in result_a.institutions}
    ids_b = {i.institution_name: i.source_id for i in result_b.institutions}
    assert ids_a == ids_b


def test_source_id_differs_across_distinct_institutions():
    csv_text = (
        "institution_name,website,contact_type,contact_value\n"
        "Beacon House School,https://beaconhouse.example.edu,phone,+923001234567\n"
        "Riverside Academy,https://riverside.example.edu,email,admissions@riverside.example.edu\n"
    )

    result = parse_authorized_import_csv(csv_text, source_reference="license-2026")

    ids = {i.source_id for i in result.institutions}
    assert len(ids) == 2
    assert all(i.startswith("license-2026:") for i in ids)
