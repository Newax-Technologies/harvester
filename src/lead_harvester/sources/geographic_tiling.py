def generate_tiles(config_yaml: dict) -> list[dict]:
    # This is a stub for phase 1. Real implementation would take city boundaries
    # and divide them into 2-4km bounding boxes.
    # For now, we just return the areas specified in the config directly.

    tiles = []
    for city, zones in config_yaml.get("cities", {}).items():
        for zone in zones:
            tiles.append({"city": city, "zone": zone, "query_prefix": f"{zone} {city}"})

    return tiles


def build_queries_for_tile(tile: dict, categories: list[str]) -> list[str]:
    from ..intelligence.taxonomy import get_synonyms

    queries = []
    for cat in categories:
        synonyms = get_synonyms(cat)
        for syn in synonyms:
            queries.append(f"{syn} in {tile['query_prefix']}")
    return queries
