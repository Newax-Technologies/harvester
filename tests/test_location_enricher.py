from lead_harvester.enrichment.location_enricher import enrich_location


def test_both_blank_returns_blank_tuple():
    assert enrich_location("", "") == ("", "")


def test_recognized_country_name_resolves_to_iso2():
    city, country_code = enrich_location("Lahore", "Pakistan")
    assert city == "Lahore"
    assert country_code == "PK"


def test_already_iso2_country_code_passes_through():
    city, country_code = enrich_location("Karachi", "PK")
    assert city == "Karachi"
    assert country_code == "PK"


def test_unrecognized_country_returns_blank_not_a_guess():
    city, country_code = enrich_location("Somewhere", "Neverland")
    assert city == "Somewhere"
    assert country_code == ""


def test_blank_locality_with_known_country():
    city, country_code = enrich_location("", "Pakistan")
    assert city == ""
    assert country_code == "PK"
