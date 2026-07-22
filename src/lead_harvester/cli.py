from __future__ import annotations

import argparse
import sys

from .config import Settings
from .pipeline import LeadPipeline

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lead-harvester",
        description="Education Infrastructure Opportunity Engine (Phase 1)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run", help="Run discovery and extraction via YAML config")
    run.add_argument("--config", required=True, help="Path to the YAML job configuration file")
    run.add_argument("--database", default="leads_v2.sqlite3")

    return parser

def run_command(args: argparse.Namespace) -> int:
    settings = Settings(
        database_path=args.database,
        job_config_path=args.config
    )
    settings.load_job_config()
    
    if not settings.google_places_api_key:
        print("Error: GOOGLE_PLACES_API_KEY environment variable is required.", file=sys.stderr)
        return 2

    pipeline = LeadPipeline(settings)
    pipeline.run()

    print(f"Finished pipeline execution using config {args.config}.")
    return 0

def main() -> None:
    args = build_parser().parse_args()
    if args.command == "run":
        raise SystemExit(run_command(args))
    raise SystemExit(2)

if __name__ == "__main__":
    main()
