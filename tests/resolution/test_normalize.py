from lead_harvester.resolution.normalize import (
    normalize_social_handle,
    normalize_website,
    social_platform_for_host,
)


def test_normalize_website_adds_missing_scheme():
    assert normalize_website("beacon.edu") == "https://beacon.edu"


def test_normalize_website_lowercases_host_only():
    # Host is lowercased for consistency, but path/query casing is left
    # alone -- some servers treat paths case-sensitively.
    assert normalize_website("https://BEACON.edu/Contact-Us") == "https://beacon.edu/Contact-Us"


def test_normalize_website_keeps_www_and_query_and_fragment():
    # Unlike normalize_domain (a bare matching key), this is a display/
    # storage value expected to actually resolve -- www./query/fragment
    # are part of that and must survive.
    assert (
        normalize_website("https://www.beacon.edu/page?x=1#section")
        == "https://www.beacon.edu/page?x=1#section"
    )


def test_normalize_website_strips_surrounding_whitespace():
    assert normalize_website("  https://beacon.edu  ") == "https://beacon.edu"


def test_normalize_website_empty_input_returns_empty_string():
    assert normalize_website("") == ""
    assert normalize_website("   ") == ""


def test_normalize_social_handle_lowercases_and_strips_www():
    assert (
        normalize_social_handle("https://WWW.LinkedIn.com/company/Example/")
        == "https://linkedin.com/company/example"
    )


def test_normalize_social_handle_adds_missing_scheme():
    assert normalize_social_handle("linkedin.com/company/example") == "https://linkedin.com/company/example"


def test_normalize_social_handle_strips_query_and_trailing_slash():
    assert (
        normalize_social_handle("https://instagram.com/example/?utm_source=ig")
        == "https://instagram.com/example"
    )


def test_normalize_social_handle_folds_twitter_into_x():
    # Same account, pre- and post-rebrand -- must produce the same key so
    # a re-scrape doesn't create a second ContactPoint for it.
    assert normalize_social_handle("https://twitter.com/example") == normalize_social_handle(
        "https://x.com/example"
    )
    assert normalize_social_handle("https://twitter.com/Example") == "https://x.com/example"


def test_normalize_social_handle_empty_input_returns_empty_string():
    assert normalize_social_handle("") == ""


def test_social_platform_for_host_recognizes_known_platforms():
    assert social_platform_for_host("https://www.linkedin.com/company/example") == "linkedin"
    assert social_platform_for_host("https://instagram.com/example") == "instagram"
    assert social_platform_for_host("https://facebook.com/example") == "facebook"
    assert social_platform_for_host("https://youtube.com/@example") == "youtube"
    assert social_platform_for_host("https://tiktok.com/@example") == "tiktok"
    assert social_platform_for_host("https://reddit.com/r/example") == "reddit"


def test_social_platform_for_host_folds_twitter_and_x_to_the_same_platform():
    assert social_platform_for_host("https://twitter.com/example") == "x"
    assert social_platform_for_host("https://x.com/example") == "x"


def test_social_platform_for_host_returns_none_for_unrecognized_host():
    assert social_platform_for_host("https://example.com/") is None
    assert social_platform_for_host("") is None
