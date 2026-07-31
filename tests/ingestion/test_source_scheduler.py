from lead_harvester.ingestion.source_scheduler import build_queries_for_tile, generate_tiles


def test_generate_tiles_expands_every_city_zone():
    config = {"cities": {"Islamabad": ["F-11", "Blue Area"], "Lahore": ["DHA"]}}

    tiles = generate_tiles(config)

    assert len(tiles) == 3
    assert {"city": "Islamabad", "zone": "F-11", "query_prefix": "F-11 Islamabad"} in tiles
    assert {"city": "Lahore", "zone": "DHA", "query_prefix": "DHA Lahore"} in tiles


def test_generate_tiles_empty_config_returns_no_tiles():
    assert generate_tiles({}) == []
    assert generate_tiles({"cities": {}}) == []


def test_build_queries_for_tile_combines_synonyms_with_the_tile_location():
    tile = {"city": "Islamabad", "zone": "F-11", "query_prefix": "F-11 Islamabad"}

    queries = build_queries_for_tile(tile, ["FORMAL_EDUCATION"])

    assert "school in F-11 Islamabad" in queries
    assert all(q.endswith("in F-11 Islamabad") for q in queries)


def test_build_queries_for_tile_unknown_category_yields_no_queries():
    tile = {"city": "Islamabad", "zone": "F-11", "query_prefix": "F-11 Islamabad"}

    assert build_queries_for_tile(tile, ["NOT_A_REAL_CATEGORY"]) == []


def test_build_queries_for_tile_combines_multiple_categories():
    tile = {"city": "Karachi", "zone": "Clifton", "query_prefix": "Clifton Karachi"}

    queries = build_queries_for_tile(tile, ["FORMAL_EDUCATION", "ACADEMIC_SUPPORT"])

    assert any("school" in q for q in queries)
    assert any("tuition center" in q for q in queries)
