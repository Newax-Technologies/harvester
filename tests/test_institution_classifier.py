from lead_harvester.enrichment.institution_classifier import classify_institution_type


def test_empty_input_returns_blank():
    assert classify_institution_type("", "") == ""


def test_classifies_school_from_name():
    assert classify_institution_type("Riverside Public School") == "school"


def test_classifies_dental_clinic_over_generic_clinic():
    assert classify_institution_type("Smile Bright Dental Clinic") == "dental_clinic"


def test_classifies_from_description_when_name_is_generic():
    assert classify_institution_type("Riverside", "A full-service law firm downtown.") == "law_firm"


def test_no_keyword_match_returns_blank():
    assert classify_institution_type("Riverside Learning Group") == ""


def test_matching_is_case_insensitive():
    assert classify_institution_type("RIVERSIDE HOSPITAL") == "hospital"
