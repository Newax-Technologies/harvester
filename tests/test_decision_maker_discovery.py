from lead_harvester.enrichment.decision_maker_discovery import discover_decision_maker


def test_empty_text_returns_none():
    assert discover_decision_maker("") is None
    assert discover_decision_maker(None) is None  # type: ignore[arg-type]


def test_no_role_keyword_returns_none():
    assert discover_decision_maker("Welcome to our school website.") is None


def test_detects_role_colon_name():
    result = discover_decision_maker("Principal: Jane Doe")
    assert result == {"name": "Jane Doe", "role": "Principal"}


def test_detects_name_comma_role():
    result = discover_decision_maker("Founded by John Smith, CEO of the company.")
    assert result == {"name": "John Smith", "role": "CEO"}


def test_detects_multi_word_role():
    result = discover_decision_maker("Contact our Managing Director: Ali Raza Khan for inquiries.")
    assert result == {"name": "Ali Raza Khan", "role": "Managing Director"}


def test_role_matching_is_case_insensitive():
    result = discover_decision_maker("principal: Jane Doe")
    assert result is not None
    assert result["name"] == "Jane Doe"
