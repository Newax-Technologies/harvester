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
    
    # We must run this in an event loop since we made pipeline async
    import asyncio
    asyncio.run(pipeline.run())

    print(f"Finished pipeline execution using config {args.config}.")
    return 0

import asyncio
from sqlalchemy import text
from .database import engine

async def check_db_health() -> int:
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("Database connection healthy.")
        return 0
    except Exception as e:
        print(f"Database connection failed: {e}", file=sys.stderr)
        return 1

def main() -> None:
    parser = build_parser()
    
    # Add db-health command
    subparsers = next(action for action in parser._actions if isinstance(action, argparse._SubParsersAction))
    subparsers.add_parser("db-health", help="Check PostgreSQL connection health")
    
    # Add migrate-phase1 command
    migrate = subparsers.add_parser("migrate-phase1", help="Migrate Phase 1 SQLite data to PostgreSQL Ledger")
    migrate.add_argument("--database", default="leads_v2.sqlite3", help="Path to Phase 1 SQLite database")
    
    # Add seed-demo-data command
    seed = subparsers.add_parser("seed-demo-data", help="Seed realistic development records")
    seed.add_argument("--reset", action="store_true", help="Truncate tables before seeding")
    seed.add_argument("--scenario", default="full", help="Scenario to seed")
    seed.add_argument("--seed", type=int, default=42, help="Random seed for deterministic output")
    
    args = parser.parse_args()
    if args.command == "run":
        raise SystemExit(run_command(args))
    elif args.command == "db-health":
        raise SystemExit(asyncio.run(check_db_health()))
    elif args.command == "migrate-phase1":
        from .migration.phase1 import migrate_phase1_data
        raise SystemExit(asyncio.run(migrate_phase1_data(args.database)))
    elif args.command == "seed-demo-data":
        from .seed import run_seed
        raise SystemExit(asyncio.run(run_seed(args)))
    raise SystemExit(2)

if __name__ == "__main__":
    main()
