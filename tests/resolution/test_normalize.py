from lead_harvester.resolution.normalize import country_to_iso2, normalize_city


def test_normalize_city_lowercases_and_strips_punctuation():
    assert normalize_city("Karachi") == "karachi"
    assert normalize_city("  New  York ") == "new york"
    assert normalize_city("St.-Louis") == "st louis"
    assert normalize_city("") == ""


def test_country_to_iso2_matches_common_names():
    assert country_to_iso2("Pakistan") == "PK"
    assert country_to_iso2("united arab emirates") == "AE"
    assert country_to_iso2("UAE") == "AE"
    assert country_to_iso2("United States of America") == "US"


def test_country_to_iso2_passes_through_a_valid_iso2_code():
    assert country_to_iso2("pk") == "PK"
    assert country_to_iso2("AE") == "AE"


def test_country_to_iso2_returns_none_for_unrecognized_or_blank():
    assert country_to_iso2("Narnia") is None
    assert country_to_iso2("") is None
    assert country_to_iso2(None) is None
