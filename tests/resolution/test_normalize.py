from lead_harvester.resolution.normalize import (
    country_to_iso2,
    normalize_city,
    normalize_domain,
    normalize_social_profile,
    normalize_website,
)


def test_normalize_domain_truncates_to_255_chars():
    # Correction regression test: every column normalize_domain's result
    # is ever written to (RawSourceRecord/RawPageSnapshot.normalized_domain,
    # CanonicalInstitution.domain) is String(255) -- an oversized netloc
    # (e.g. embedded userinfo, an unreasonably long host) must not reach
    # a flush-time "value too long" error that aborts an entire crawler
    # run over one bad seed URL.
    huge_host = "a" * 300 + ".example.edu"
    result = normalize_domain(f"https://{huge_host}/path")
    assert len(result) == 255
    assert result == huge_host[:255]


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


def test_normalize_website_adds_missing_scheme():
    assert normalize_website("example.edu") == "https://example.edu"


def test_normalize_website_preserves_explicit_http_scheme():
    # Some institutions genuinely only serve http -- forcing https would
    # store a URL that doesn't actually match what the site serves.
    assert normalize_website("http://example.edu") == "http://example.edu"


def test_normalize_website_lowercases_host_and_strips_www_and_trailing_slash():
    assert normalize_website("WWW.Example.EDU/") == "https://example.edu"


def test_normalize_website_keeps_a_real_path_and_query():
    assert (
        normalize_website("https://www.example.edu/admissions?year=2026")
        == "https://example.edu/admissions?year=2026"
    )


def test_normalize_website_returns_empty_for_blank_input():
    assert normalize_website("") == ""
    assert normalize_website("   ") == ""


def test_normalize_social_profile_maps_known_platforms_to_contact_type():
    assert normalize_social_profile("https://www.facebook.com/SomePage/") == (
        "facebook",
        "https://facebook.com/SomePage",
    )
    assert normalize_social_profile("https://x.com/SomeHandle") == (
        "twitter",
        "https://x.com/SomeHandle",
    )
    assert normalize_social_profile("https://www.linkedin.com/company/beacon-school") == (
        "linkedin",
        "https://linkedin.com/company/beacon-school",
    )


def test_normalize_social_profile_strips_query_and_fragment_for_dedup():
    assert normalize_social_profile("https://instagram.com/beaconschool?hl=en#bio") == (
        "instagram",
        "https://instagram.com/beaconschool",
    )


def test_normalize_social_profile_returns_none_for_bare_platform_homepage():
    assert normalize_social_profile("https://www.facebook.com/") is None
    assert normalize_social_profile("https://www.facebook.com") is None


def test_normalize_social_profile_returns_none_for_unrecognized_host():
    assert normalize_social_profile("https://example.edu/about") is None
    assert normalize_social_profile("") is None
