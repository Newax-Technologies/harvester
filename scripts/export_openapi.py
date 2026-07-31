import json
import sys

from fastapi.openapi.utils import get_openapi

from lead_harvester.api.app import app


def export_openapi(filepath: str):
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
    )
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python export_openapi.py <output.json>")
        sys.exit(1)
    export_openapi(sys.argv[1])
    print(f"Exported OpenAPI schema to {sys.argv[1]}")
