from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from .config import Settings
from .database import engine
from .pipeline import LeadPipeline

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _env(key: str, default: str = "") -> str:
    import os

    return os.getenv(key, default)


# ---------------------------------------------------------------------------
# Command implementations
# ---------------------------------------------------------------------------


def run_command(args: argparse.Namespace) -> int:
    settings = Settings(job_config_path=args.config)
    settings.load_job_config()

    job_config = settings.job_config
    places_provider = job_config.get("places_provider")
    has_tile_based_provider_config = (
        (places_provider in (None, "google") and settings.google_places_api_key)
        or (places_provider == "apple" and settings.apple_maps_team_id)
        or (places_provider == "yandex" and settings.yandex_maps_api_key)
    )
    if (
        "seeds" not in job_config
        and "search_queries" not in job_config
        and "telegram_channels" not in job_config
        and not has_tile_based_provider_config
    ):
        print(
            "Error: job.yaml must contain 'seeds', 'search_queries', or "
            "'telegram_channels', or the credentials for job.yaml's places_provider "
            "(default 'google': GOOGLE_PLACES_API_KEY; 'apple': "
            "APPLE_MAPS_TEAM_ID/KEY_ID/PRIVATE_KEY; 'yandex': YANDEX_MAPS_API_KEY) must "
            "be set.",
            file=sys.stderr,
        )
        return 2

    pipeline = LeadPipeline(settings)
    asyncio.run(pipeline.run())
    print(f"Finished pipeline execution using config {args.config}.")
    return 0


async def import_authorized(args: argparse.Namespace) -> int:
    """
    Bulk-imports institutions/contacts from a licensed or manually-sourced
    CSV via LeadPipeline._run_authorized_import -- the same
    blocking/scoring resolution every other connector goes through, so
    imported rows correctly dedupe/merge against existing institutions
    rather than each becoming its own separate entity.
    """
    if not Path(args.file).exists():
        print(f"CSV file not found: {args.file}", file=sys.stderr)
        return 1

    job_config: dict = {
        "authorized_import_file": args.file,
        "authorized_import_source_reference": args.source_reference,
    }
    settings = Settings(job_config=job_config)
    if args.country_code:
        settings.lead_sync_default_country_code = args.country_code.upper()

    pipeline = LeadPipeline(settings)
    success = await pipeline.run()
    return 0 if success else 1


async def check_db_health() -> int:
    from sqlalchemy import text

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("Database connection healthy.")
        return 0
    except Exception as e:
        print(f"Database connection failed: {e}", file=sys.stderr)
        return 1


# ---------------------------------------------------------------------------
# LinkedIn commands
# ---------------------------------------------------------------------------


async def linkedin_login(args: argparse.Namespace) -> int:
    """
    Open a real (visible) Camoufox browser, navigate to linkedin.com/login,
    and wait for the user to log in manually. Then saves the session cookies.
    """
    try:
        from camoufox.async_api import AsyncCamoufox
    except ImportError:
        print("camoufox not installed. Run: pip install 'camoufox[geoip]'", file=sys.stderr)
        return 1

    from .sources.session_manager import SessionManager

    account_id = args.account
    sm = SessionManager("sessions")

    print(f"\n{'=' * 60}")
    print(f"  LinkedIn Login — Account: {account_id}")
    print(f"{'=' * 60}")
    print("A browser will open. Log in to LinkedIn manually.")
    print("Once you are on the LinkedIn feed page, come back here")
    print("and press ENTER to save your session.\n")

    async with AsyncCamoufox(headless=False, humanize=True, addons=[]) as browser:
        context = await browser.new_context(
            locale="en-US",
            timezone_id="Asia/Karachi",
        )
        page = await context.new_page()
        await page.goto("https://www.linkedin.com/login", wait_until="networkidle")

        input(">>> Press ENTER after you have logged in successfully...")

        cookies = await context.cookies()
        sm.save_cookies(account_id, cookies, first_login=True)
        await context.close()

    print(f"\n✓ Session saved for account '{account_id}'. You can now run linkedin-run.\n")
    return 0


async def linkedin_run(args: argparse.Namespace) -> int:
    """
    Crawl a list of LinkedIn profile URLs using the stealth crawler.
    Profile URLs are read from a plain-text file (one URL per line).
    """
    import dataclasses

    from .database import get_session
    from .models import RawSourceRecord
    from .models.source import SourceType
    from .sources.linkedin_stealth import LinkedInStealthCrawler

    account_id = args.account
    proxy = args.proxy or _env("LINKEDIN_PROXY")
    captcha_key = args.captcha_key or _env("TWOCAPTCHA_API_KEY")

    try:
        text = await asyncio.to_thread(Path(args.urls_file).read_text)
        urls = [line.strip() for line in text.splitlines() if line.strip().startswith("http")]
    except FileNotFoundError:
        print(f"URLs file not found: {args.urls_file}", file=sys.stderr)
        return 1

    if not urls:
        print("No valid URLs found in file.", file=sys.stderr)
        return 1

    print(f"[LinkedIn] Starting stealth crawl of {len(urls)} profile(s)...")
    crawler = LinkedInStealthCrawler(
        account_id=account_id,
        target_urls=urls,
        captcha_api_key=captcha_key or None,
        proxy=proxy or None,
    )
    crawl_aborted = False
    try:
        profiles = await crawler.run()
    except Exception as e:
        # A CAPTCHA-triggered abort, a search-budget exhaustion, or any
        # other browser-level failure escaping run() after earlier URLs
        # already succeeded previously lost every profile harvested so
        # far -- this method never reached the persistence block below at
        # all. run() attaches whatever it collected before the exception
        # to partial_profiles; persist that instead of discarding it.
        profiles = getattr(e, "partial_profiles", None)
        if profiles is None:
            raise
        print(
            f"[LinkedIn] Crawl aborted ({e}) -- persisting {len(profiles)} "
            "profile(s) collected before the abort.",
            file=sys.stderr,
        )
        crawl_aborted = True

    # Persist raw profiles to database
    async with get_session() as session:
        from .models.source import RunStatus, SourceRun

        run = SourceRun(
            source_type=SourceType.LINKEDIN,
            run_metadata={"profiles_found": len(profiles), "urls_attempted": len(urls)},
            status=RunStatus.STARTED,
        )
        session.add(run)
        await session.flush()

        # Each row gets its own SAVEPOINT (see docs/CODE_REVIEW_LESSONS.md
        # pattern 3) -- a single profile failing a DB-level constraint must
        # not abort every other already-added profile in this same shared
        # session, discarding an entire crawl's worth of harvested profiles
        # over one bad row.
        saved_count = 0
        for profile in profiles:
            try:
                async with session.begin_nested():
                    session.add(
                        RawSourceRecord(
                            source_run_id=run.id,
                            source_type=SourceType.LINKEDIN,
                            source_id=profile.profile_url,
                            raw_payload=dataclasses.asdict(profile),
                            normalized_name=profile.full_name or profile.company,
                            normalized_phone=None,
                            normalized_domain=None,
                            location=None,
                        )
                    )
                    await session.flush()
                saved_count += 1
            except Exception as e:
                print(f"[LinkedIn] Failed to persist profile {profile.profile_url}: {e}")

        import datetime as dt

        from .models.source import RunStatus

        run.status = RunStatus.COMPLETED
        run.completed_at = dt.datetime.now(dt.UTC)

    print(f"\n✓ Saved {saved_count} of {len(profiles)} profiles to database.")
    print("  Run `linkedin-research` next to analyse them with AI.\n")
    return 1 if crawl_aborted else 0


async def linkedin_research(args: argparse.Namespace) -> int:
    """
    Run the AI Research Brain on all unprocessed LinkedIn profiles.
    """
    from .intelligence.researcher import ResearchBrain

    api_key = args.openai_key or _env("OPENAI_API_KEY")
    if not api_key:
        print(
            "Error: OPENAI_API_KEY is required. Set it in .env or pass --openai-key.",
            file=sys.stderr,
        )
        return 1

    brain = ResearchBrain(api_key=api_key, model=args.model)
    print("[Research] Processing pending LinkedIn profiles...")
    await brain.process_all_pending()
    print("\n✓ Research complete. Check your dashboard for AccountBrief records.\n")
    return 0


async def qualify_leads(args: argparse.Namespace) -> int:
    """
    Run QualificationAgent against every institution that has never been
    assessed, then refresh each one's LeadProfile. Previously
    QualificationAgent existed but had no caller anywhere in the live
    pipeline -- this is the first invokable path for it.
    """
    from .database import get_session
    from .services.lead_profile_service import qualify_all_unassessed

    async with get_session() as session:
        count = await qualify_all_unassessed(
            session, criteria_version=args.criteria_version, limit=args.limit
        )

    print(f"\n✓ Qualified {count} institution(s). Check lead profiles for updated scores.\n")
    return 0


async def select_daily_leads(args: argparse.Namespace) -> int:
    """
    Claim a batch of the highest-scoring eligible leads for a round of
    outreach work (docs/ROADMAP.md module 10). Prints each reserved
    institution and its score/batch label.
    """
    from .database import get_session
    from .services.daily_selection_service import select_daily_batch

    async with get_session() as session:
        reservations = await select_daily_batch(
            session,
            limit=args.limit,
            ttl_hours=args.ttl_hours,
            min_score=args.min_score,
            batch_label=args.batch_label,
        )
        # Captured before the session closes -- ORM attribute access after
        # that would need a live connection to lazy-load anything not
        # already resident.
        summary = [
            (r.institution_id, r.score_at_reservation, r.batch_label, r.expires_at)
            for r in reservations
        ]

    print(f"\n[DailySelection] Reserved {len(summary)} lead(s):")
    for institution_id, score, batch_label, expires_at in summary:
        print(f"  {institution_id}  score={score}  batch={batch_label}  expires={expires_at}")
    print()
    return 0


async def verify_data_quality(args: argparse.Namespace) -> int:
    """
    Run verification checks (confidence drift, conflicting canonical_name
    assertions, stale evidence) across a batch of institutions, creating
    DataQualityFlag rows for anything found (docs/ROADMAP.md module 12).
    """
    from .database import get_session
    from .services.verification_service import run_verification_sweep

    async with get_session() as session:
        created_count = await run_verification_sweep(
            session, limit=args.limit, freshness_days=args.freshness_days
        )

    print(f"\n[Verification] Created {created_count} new data-quality flag(s).\n")
    return 0


async def suppress_contact(args: argparse.Namespace) -> int:
    """Add a phone/email/LinkedIn URL to the do-not-contact suppression list (docs/ROADMAP.md module 11)."""
    from .database import get_session
    from .models.compliance import SuppressionReason
    from .services.compliance_service import add_suppression

    async with get_session() as session:
        entry = await add_suppression(
            session,
            args.contact_value,
            SuppressionReason(args.reason),
            channel=args.channel,
            note=args.note,
            suppressed_by="cli",
        )
        normalized = entry.normalized_contact_value

    print(f"\n[Compliance] Suppressed {normalized!r} (channel={args.channel or 'all'}).\n")
    return 0


async def purge_expired_records(args: argparse.Namespace) -> int:
    """Delete RawSourceRecord rows past retention that never produced provenance (docs/ROADMAP.md module 11)."""
    from .database import get_session
    from .services.compliance_service import purge_expired_raw_records

    async with get_session() as session:
        deleted_count = await purge_expired_raw_records(session, retention_days=args.retention_days)

    print(f"\n[Compliance] Purged {deleted_count} expired, unreferenced raw record(s).\n")
    return 0


async def process_outbox(args: argparse.Namespace) -> int:
    """
    Retry PENDING event_outbox rows whose next_attempt_at has passed
    (docs/ROADMAP.md module 13). Intended to run on a schedule (e.g. cron
    every few minutes) alongside the immediate delivery attempt every
    enqueue already makes, so a delivery that failed on its first attempt
    still gets retried without a human doing anything.
    """
    from .api.dependencies import get_lead_sync_emitter
    from .database import get_session
    from .services.outbox_service import process_pending_deliveries

    emitter = get_lead_sync_emitter()
    async with get_session() as session:
        processed = await process_pending_deliveries(session, emitter, limit=args.limit)

    print(f"\n[Outbox] Attempted delivery for {processed} pending event(s).\n")
    return 0


async def export_leads(args: argparse.Namespace) -> int:
    """
    Export institutions/contacts as CSV or JSON (docs/ROADMAP.md module 13).
    Writes to --output if given, otherwise prints to stdout.
    """
    from .database import get_session
    from .exports import build_lead_export_rows, rows_to_csv, rows_to_json
    from .models.canonical import OperatingStatus
    from .models.qualification import QualificationStatus

    async with get_session() as session:
        rows = await build_lead_export_rows(
            session,
            status=OperatingStatus(args.status) if args.status else None,
            min_score=args.min_score,
            qualification_status=(
                QualificationStatus(args.qualification_status)
                if args.qualification_status
                else None
            ),
            limit=args.limit,
        )

    content = rows_to_csv(rows) if args.format == "csv" else rows_to_json(rows)
    if args.output:
        Path(args.output).write_text(content)
        print(f"\n[Export] Wrote {len(rows)} row(s) to {args.output}.\n")
    else:
        print(content)
    return 0


async def ops_health(args: argparse.Namespace) -> int:
    """Print a real health signal: DB reachability + any SourceRuns stuck in STARTED (docs/ROADMAP.md module 15)."""
    from .database import get_session
    from .services.operations_service import check_health

    async with get_session() as session:
        result = await check_health(session)

    status = "HEALTHY" if result["healthy"] else "UNHEALTHY"
    print(f"\n[Health] {status}")
    print(f"  database_ok: {result['database_ok']}")
    print(f"  stuck_run_count: {result['stuck_run_count']}")
    if result["stuck_run_ids"]:
        print(f"  stuck_run_ids: {', '.join(result['stuck_run_ids'])}")
    print()
    return 0 if result["healthy"] else 1


async def ops_metrics(args: argparse.Namespace) -> int:
    """Print aggregated operational counts across every module (docs/ROADMAP.md module 15)."""
    from .database import get_session
    from .services.operations_service import compute_operational_metrics

    async with get_session() as session:
        metrics = await compute_operational_metrics(session)

    print("\n[Metrics]")
    for key, value in metrics.items():
        if key == "recent_pipeline_activity":
            continue
        print(f"  {key}: {value}")
    print()
    return 0


async def ops_source_health(args: argparse.Namespace) -> int:
    """Print per-source-type run health (docs/ROADMAP.md module 15)."""
    from .database import get_session
    from .services.operations_service import compute_source_health

    async with get_session() as session:
        health = await compute_source_health(session)

    print("\n[Source Health]")
    for entry in health:
        print(
            f"  {entry['source_type']}: last_run={entry['last_run_status']} "
            f"at {entry['last_run_at']}, last_success={entry['last_successful_run_at']}, "
            f"failed_last_7d={entry['failed_run_count_last_7d']}"
        )
    print()
    return 0


async def ops_page_snapshots(args: argparse.Namespace) -> int:
    """List raw page-fetch snapshots from WEBSITE crawls (docs/ROADMAP.md module 3)."""
    import uuid as uuid_module

    from .database import get_session
    from .services.operations_service import list_page_snapshots

    source_run_id = uuid_module.UUID(args.source_run_id) if args.source_run_id else None

    async with get_session() as session:
        snapshots = await list_page_snapshots(
            session, source_run_id=source_run_id, only_errors=args.only_errors, limit=args.limit
        )

    print(f"\n[Page Snapshots] {len(snapshots)} found")
    for snapshot in snapshots:
        status = snapshot.fetch_error or f"HTTP {snapshot.status_code}"
        print(f"  {snapshot.fetched_at} {snapshot.url} -> {status}")
    print()
    return 0


async def list_person_candidates_cmd(args: argparse.Namespace) -> int:
    """List discovered person candidates, most recently seen first (docs/ROADMAP.md module 1)."""
    import uuid as uuid_module

    from .database import get_session
    from .services.person_candidate_service import list_person_candidates

    async with get_session() as session:
        candidates = await list_person_candidates(
            session,
            institution_id=uuid_module.UUID(args.institution_id) if args.institution_id else None,
            limit=args.limit,
        )
        summary = [
            (c.id, c.institution_id, c.display_name, c.evidence_count, c.status.value)
            for c in candidates
        ]

    print(f"\n[PersonCandidates] {len(summary)} candidate(s):")
    for cid, institution_id, display_name, evidence_count, status in summary:
        print(
            f"  {cid}  institution={institution_id}  {display_name!r}  "
            f"evidence={evidence_count}  status={status}"
        )
    print()
    return 0


async def list_signals_cmd(args: argparse.Namespace) -> int:
    """List detected pain-point/buying-signal rows, most recent first (docs/ROADMAP.md module 1)."""
    import uuid as uuid_module

    from .database import get_session
    from .models.signal import SignalType
    from .services.signal_service import list_signals

    async with get_session() as session:
        signals = await list_signals(
            session,
            institution_id=uuid_module.UUID(args.institution_id) if args.institution_id else None,
            signal_type=SignalType(args.signal_type) if args.signal_type else None,
            limit=args.limit,
        )
        summary = [(s.id, s.institution_id, s.signal_type.value, s.signal_text) for s in signals]

    print(f"\n[Signals] {len(summary)} signal(s):")
    for sid, institution_id, signal_type, signal_text in summary:
        print(f"  {sid}  institution={institution_id}  [{signal_type}]  {signal_text}")
    print()
    return 0


async def linkedin_send(args: argparse.Namespace) -> int:
    """
    Send all approved OutreachDraft records (LinkedIn messages or emails).
    """
    from .outreach.automator import OutreachAutomator

    automator = OutreachAutomator(
        account_id=args.account,
        smtp_host=args.smtp_host or _env("SMTP_HOST"),
        smtp_port=int(args.smtp_port or _env("SMTP_PORT", "587")),
        smtp_user=args.smtp_user or _env("SMTP_USER"),
        smtp_password=_env("SMTP_PASSWORD"),
        smtp_from_name=args.from_name or _env("SMTP_FROM_NAME", "NEWAX Sales"),
        captcha_api_key=_env("TWOCAPTCHA_API_KEY") or None,
        proxy=args.proxy or _env("LINKEDIN_PROXY") or None,
        dry_run=args.dry_run,
    )

    mode = "DRY RUN" if args.dry_run else "LIVE"
    print(f"[Outreach] Starting automator ({mode})...")
    await automator.run()
    return 0


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lead-harvester",
        description="Education Infrastructure Opportunity Engine",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # -- run (web / Google Places) ----------------------------------------
    run = subparsers.add_parser("run", help="Run discovery via YAML config (web / Google Places)")
    run.add_argument("--config", required=True, help="Path to the YAML job config file")

    # -- import-authorized ---------------------------------------------------
    import_authorized = subparsers.add_parser(
        "import-authorized",
        help="Bulk-import institutions/contacts from a licensed or manually-sourced CSV",
    )
    import_authorized.add_argument("--file", required=True, help="Path to the CSV file to import")
    import_authorized.add_argument(
        "--source-reference",
        required=True,
        help="Identifies the license/agreement or manual-research source this data came from",
    )
    import_authorized.add_argument(
        "--country-code",
        default="",
        help="ISO-2 fallback country code for rows with a blank country_code column (default: PK)",
    )

    # -- db-health ----------------------------------------------------------
    subparsers.add_parser("db-health", help="Check PostgreSQL connection health")

    # -- migrate-phase1 -----------------------------------------------------
    migrate = subparsers.add_parser(
        "migrate-phase1", help="Migrate Phase 1 SQLite data to PostgreSQL"
    )
    migrate.add_argument("--database", default="leads_v2.sqlite3")

    # -- seed-demo-data -----------------------------------------------------
    seed = subparsers.add_parser("seed-demo-data", help="Seed realistic dev records")
    seed.add_argument("--reset", action="store_true")
    seed.add_argument("--scenario", default="full")
    seed.add_argument("--seed", type=int, default=42)

    # -- linkedin-login -----------------------------------------------------
    li_login = subparsers.add_parser(
        "linkedin-login",
        help="Open browser, log in to LinkedIn manually, save session cookies",
    )
    li_login.add_argument(
        "--account", required=True, help="Burner account identifier (e.g. burner_01)"
    )

    # -- linkedin-run -------------------------------------------------------
    li_run = subparsers.add_parser(
        "linkedin-run",
        help="Stealthily crawl LinkedIn profiles (reads URLs from a text file)",
    )
    li_run.add_argument("--account", required=True, help="Burner account identifier")
    li_run.add_argument(
        "--urls-file", required=True, help="Text file with one LinkedIn profile URL per line"
    )
    li_run.add_argument(
        "--proxy", default="", help="Residential proxy (http://user:pass@host:port)"
    )
    li_run.add_argument("--captcha-key", default="", help="2Captcha API key")

    # -- linkedin-research --------------------------------------------------
    li_research = subparsers.add_parser(
        "linkedin-research",
        help="Run AI Research Brain on extracted LinkedIn profiles",
    )
    li_research.add_argument(
        "--openai-key", default="", help="OpenAI API key (or set OPENAI_API_KEY)"
    )
    li_research.add_argument("--model", default="gpt-4o-mini", help="OpenAI model name")

    # -- qualify-leads --------------------------------------------------------
    qualify = subparsers.add_parser(
        "qualify-leads",
        help="Run QualificationAgent against every institution never assessed, and refresh profiles",
    )
    qualify.add_argument(
        "--criteria-version", type=int, default=1, help="Qualification criteria version to record"
    )
    qualify.add_argument(
        "--limit", type=int, default=200, help="Max unassessed institutions to process this run"
    )

    # -- select-daily-leads ---------------------------------------------------
    select_daily = subparsers.add_parser(
        "select-daily-leads",
        help="Claim a batch of the highest-scoring eligible leads for outreach work",
    )
    select_daily.add_argument(
        "--limit", type=int, default=None, help="Max leads to reserve (default: settings)"
    )
    select_daily.add_argument(
        "--ttl-hours",
        type=float,
        default=None,
        help="Hours before an unconsumed reservation expires (default: settings)",
    )
    select_daily.add_argument(
        "--min-score", type=int, default=None, help="Minimum overall_score to be eligible"
    )
    select_daily.add_argument(
        "--batch-label", default=None, help="Label for this batch (default: today's date)"
    )

    # -- verify-data-quality --------------------------------------------------
    verify = subparsers.add_parser(
        "verify-data-quality",
        help="Run verification checks (confidence drift, conflicts, staleness) across institutions",
    )
    verify.add_argument("--limit", type=int, default=200, help="Max institutions to check this run")
    verify.add_argument(
        "--freshness-days",
        type=int,
        default=90,
        help="Flag an institution with no evidence recorded within this many days",
    )

    # -- suppress-contact -------------------------------------------------
    suppress = subparsers.add_parser(
        "suppress-contact",
        help="Add a phone/email/LinkedIn URL to the do-not-contact suppression list",
    )
    suppress.add_argument("contact_value", help="Phone, email, or LinkedIn URL to suppress")
    suppress.add_argument(
        "--reason",
        choices=["opt_out", "bounced", "legal_request", "manual"],
        default="manual",
    )
    suppress.add_argument(
        "--channel", default=None, help="Limit to one channel (e.g. 'email'); default: all channels"
    )
    suppress.add_argument("--note", default="")

    # -- purge-expired-records ----------------------------------------------
    purge = subparsers.add_parser(
        "purge-expired-records",
        help="Delete RawSourceRecord rows past the retention window that never produced provenance",
    )
    purge.add_argument(
        "--retention-days",
        type=int,
        default=365,
        help="Delete unreferenced records older than this",
    )

    # -- process-outbox -----------------------------------------------------
    process_outbox_parser = subparsers.add_parser(
        "process-outbox",
        help="Retry PENDING lead_sync outbox rows whose next_attempt_at has passed",
    )
    process_outbox_parser.add_argument(
        "--limit", type=int, default=50, help="Max outbox rows to attempt this run"
    )

    # -- export-leads ---------------------------------------------------------
    export_leads_parser = subparsers.add_parser(
        "export-leads",
        help="Export institutions/contacts as CSV or JSON",
    )
    export_leads_parser.add_argument("--format", choices=["csv", "json"], default="csv")
    export_leads_parser.add_argument(
        "--output", default=None, help="File to write to (default: print to stdout)"
    )
    export_leads_parser.add_argument(
        "--status",
        choices=["operational", "closed_temporarily", "closed_permanently", "unknown"],
        default=None,
        help="Filter to institutions with this operating status",
    )
    export_leads_parser.add_argument(
        "--min-score", type=int, default=None, help="Minimum LeadProfile.overall_score"
    )
    export_leads_parser.add_argument(
        "--qualification-status",
        choices=["pending", "qualified", "disqualified", "needs_review"],
        default=None,
    )
    export_leads_parser.add_argument(
        "--limit", type=int, default=1000, help="Max institutions to include"
    )

    # -- ops-health -----------------------------------------------------------
    subparsers.add_parser(
        "ops-health",
        help="Check DB reachability and surface any SourceRuns stuck in STARTED",
    )

    # -- ops-metrics ------------------------------------------------------------
    subparsers.add_parser(
        "ops-metrics",
        help="Print aggregated operational counts across every module",
    )

    # -- ops-source-health --------------------------------------------------
    subparsers.add_parser(
        "ops-source-health",
        help="Print per-source-type run health (last run, last success, recent failures)",
    )

    # -- ops-page-snapshots -----------------------------------------------------
    ops_page_snapshots_parser = subparsers.add_parser(
        "ops-page-snapshots",
        help="List raw page-fetch snapshots from WEBSITE crawls",
    )
    ops_page_snapshots_parser.add_argument(
        "--source-run-id", default=None, help="Filter to one SourceRun's snapshots"
    )
    ops_page_snapshots_parser.add_argument(
        "--only-errors", action="store_true", help="Only show failed/skipped fetches"
    )
    ops_page_snapshots_parser.add_argument("--limit", type=int, default=100)

    # -- list-person-candidates -----------------------------------------------
    list_person_candidates_parser = subparsers.add_parser(
        "list-person-candidates",
        help="List discovered person candidates",
    )
    list_person_candidates_parser.add_argument(
        "--institution-id", default=None, help="Filter to one institution"
    )
    list_person_candidates_parser.add_argument("--limit", type=int, default=100)

    # -- list-signals -----------------------------------------------------------
    list_signals_parser = subparsers.add_parser(
        "list-signals",
        help="List detected pain-point/buying-signal rows",
    )
    list_signals_parser.add_argument(
        "--institution-id", default=None, help="Filter to one institution"
    )
    list_signals_parser.add_argument(
        "--signal-type", choices=["pain_point", "buying_signal"], default=None
    )
    list_signals_parser.add_argument("--limit", type=int, default=100)

    # -- linkedin-send ------------------------------------------------------
    li_send = subparsers.add_parser(
        "linkedin-send",
        help="Send approved outreach drafts via LinkedIn message and/or email",
    )
    li_send.add_argument("--account", required=True, help="Burner account identifier")
    li_send.add_argument("--smtp-host", default="", help="SMTP host (or set SMTP_HOST)")
    li_send.add_argument("--smtp-port", default="587")
    li_send.add_argument("--smtp-user", default="", help="SMTP username / email")
    li_send.add_argument("--from-name", default="", help="Display name in From header")
    li_send.add_argument("--proxy", default="")
    li_send.add_argument(
        "--dry-run", action="store_true", help="Type messages but do NOT click Send"
    )

    # -- linkedin-status ----------------------------------------------------
    li_status = subparsers.add_parser(
        "linkedin-status",
        help="Show warmup phase, account age, and today's action limits",
    )
    li_status.add_argument("--account", required=True, help="Burner account identifier")

    # -- linkedin-farm-run -------------------------------------------------
    li_farm = subparsers.add_parser(
        "linkedin-farm-run",
        help="Distribute URLs across multiple accounts (each in its own browser process)",
    )
    li_farm.add_argument(
        "--accounts",
        required=True,
        help="Comma-separated list of account IDs (e.g. burner_01,burner_02,burner_03)",
    )
    li_farm.add_argument(
        "--urls-file", required=True, help="Text file with one LinkedIn profile URL per line"
    )
    li_farm.add_argument(
        "--proxies-file",
        default="",
        help="Text file with one proxy per line (format: account_id=http://user:pass@host:port)",
    )
    li_farm.add_argument("--captcha-key", default="", help="2Captcha API key")
    li_farm.add_argument(
        "--vertical",
        default="",
        help=(
            "Declares what --urls-file targets (e.g. 'school_principals'), enforcing "
            "the 30-day cross-account breadth ceiling for this (vertical, --target-city) "
            "combination. Defaults to 'unknown' if omitted."
        ),
    )
    li_farm.add_argument(
        "--target-city",
        default="",
        help=(
            "Declares which city --urls-file targets (e.g. 'karachi'), paired with "
            "--vertical for the breadth ceiling. Defaults to 'unknown' if omitted."
        ),
    )
    li_farm.add_argument(
        "--noise-urls-file",
        default="",
        help=(
            "Optional text file of off-target-vertical LinkedIn profile URLs, one per "
            "line. Used to satisfy an account's due noise visit (industry mixing) "
            "before its next real target visit."
        ),
    )

    # -- linkedin-farm-status ----------------------------------------------
    li_farm_status = subparsers.add_parser(
        "linkedin-farm-status",
        help="Show warmup phase and identity summary for all farm accounts",
    )
    li_farm_status.add_argument(
        "--accounts", required=True, help="Comma-separated list of account IDs"
    )

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        "run": lambda: sys.exit(run_command(args)),
        "import-authorized": lambda: sys.exit(asyncio.run(import_authorized(args))),
        "db-health": lambda: sys.exit(asyncio.run(check_db_health())),
        "migrate-phase1": lambda: sys.exit(asyncio.run(_migrate(args))),
        "seed-demo-data": lambda: sys.exit(asyncio.run(_seed(args))),
        "linkedin-login": lambda: sys.exit(asyncio.run(linkedin_login(args))),
        "linkedin-run": lambda: sys.exit(asyncio.run(linkedin_run(args))),
        "linkedin-research": lambda: sys.exit(asyncio.run(linkedin_research(args))),
        "qualify-leads": lambda: sys.exit(asyncio.run(qualify_leads(args))),
        "select-daily-leads": lambda: sys.exit(asyncio.run(select_daily_leads(args))),
        "verify-data-quality": lambda: sys.exit(asyncio.run(verify_data_quality(args))),
        "suppress-contact": lambda: sys.exit(asyncio.run(suppress_contact(args))),
        "purge-expired-records": lambda: sys.exit(asyncio.run(purge_expired_records(args))),
        "process-outbox": lambda: sys.exit(asyncio.run(process_outbox(args))),
        "export-leads": lambda: sys.exit(asyncio.run(export_leads(args))),
        "ops-health": lambda: sys.exit(asyncio.run(ops_health(args))),
        "ops-metrics": lambda: sys.exit(asyncio.run(ops_metrics(args))),
        "ops-source-health": lambda: sys.exit(asyncio.run(ops_source_health(args))),
        "ops-page-snapshots": lambda: sys.exit(asyncio.run(ops_page_snapshots(args))),
        "list-person-candidates": lambda: sys.exit(asyncio.run(list_person_candidates_cmd(args))),
        "list-signals": lambda: sys.exit(asyncio.run(list_signals_cmd(args))),
        "linkedin-send": lambda: sys.exit(asyncio.run(linkedin_send(args))),
        "linkedin-status": lambda: _linkedin_status(args),
        "linkedin-farm-run": lambda: sys.exit(asyncio.run(_linkedin_farm_run(args))),
        "linkedin-farm-status": lambda: _linkedin_farm_status(args),
    }

    handler = dispatch.get(args.command)
    if handler:
        handler()
    else:
        sys.exit(2)


def _linkedin_status(args: argparse.Namespace) -> None:
    from .sources.session_manager import SessionManager

    sm = SessionManager("sessions")
    if not sm.has_session(args.account):
        print(f"No session found for '{args.account}'. Run linkedin-login first.")
        return
    sm.print_status(args.account)


async def _linkedin_farm_run(args: argparse.Namespace) -> int:
    from .sources.account_farm import AccountFarm

    accounts = [a.strip() for a in args.accounts.split(",") if a.strip()]
    captcha_key = args.captcha_key or _env("TWOCAPTCHA_API_KEY") or None

    # Load proxy map from file (format: burner_01=http://user:pass@host:port)
    proxies: dict[str, str] = {}
    if args.proxies_file:
        try:
            for line in Path(args.proxies_file).read_text().splitlines():
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    acc, proxy = line.split("=", 1)
                    proxies[acc.strip()] = proxy.strip()
        except FileNotFoundError:
            # An operator who explicitly asked for --proxies-file wants
            # every account launched behind a residential proxy -- silently
            # continuing with an empty map would expose the host's real IP
            # and let LinkedIn correlate every "isolated" burner account by
            # shared origin, exactly what the proxy was meant to prevent.
            print(f"Proxies file not found: {args.proxies_file}", file=sys.stderr)
            return 1

        # A file that exists but omits one of the requested accounts (or has
        # a malformed line for it -- no "=", or a blank value after it) still
        # leaves that account missing from the map. account_farm.py's lookup
        # (self.proxies.get(account_id)) silently returns None for it, and
        # that one worker launches unproxied from the host's real IP --
        # exactly the cross-account correlation risk the proxies file exists
        # to prevent. Reject the whole run up front instead of discovering
        # the gap only after an account already ran exposed.
        missing = [acc for acc in accounts if not proxies.get(acc)]
        if missing:
            print(
                f"Proxies file {args.proxies_file} has no proxy configured for "
                f"account(s): {', '.join(missing)}",
                file=sys.stderr,
            )
            return 1

    # Load URLs
    try:
        urls = [
            l.strip()
            for l in Path(args.urls_file).read_text().splitlines()
            if l.strip().startswith("http")
        ]
    except FileNotFoundError:
        print(f"URLs file not found: {args.urls_file}", file=sys.stderr)
        return 1

    if not urls:
        print("No valid URLs found in file.", file=sys.stderr)
        return 1

    # Optional pool of off-target-vertical profiles for noise injection --
    # unlike --urls-file/--proxies-file, a missing file here just means no
    # noise pool is available (needs_noise_visit silently has nothing to
    # satisfy, same as before this feature existed), not a hard failure --
    # noise injection is a best-effort mitigation, not a requirement to run.
    noise_urls: list[str] = []
    if args.noise_urls_file:
        try:
            noise_urls = [
                l.strip()
                for l in Path(args.noise_urls_file).read_text().splitlines()
                if l.strip().startswith("http")
            ]
        except FileNotFoundError:
            print(f"Noise URLs file not found: {args.noise_urls_file}", file=sys.stderr)
            return 1

    farm = AccountFarm(accounts=accounts, proxies=proxies, captcha_key=captcha_key)
    results = await farm.run(
        urls,
        vertical=args.vertical or "unknown",
        target_city=args.target_city or "unknown",
        noise_urls=noise_urls or None,
    )

    # An empty results list means run() legitimately skipped the whole day
    # (outside working hours, or a weekend) -- not a failure. Otherwise, if
    # every single account reported an error (missing session, browser
    # crash, or a timed-out worker -- see the synthetic entries run() now
    # adds for those), a scheduler previously still saw exit code 0 and
    # recorded a fully-failed harvest as successful.
    if results and all(r.errors for r in results):
        print(
            f"[Farm] All {len(results)} account(s) failed this run -- see errors above.",
            file=sys.stderr,
        )
        return 1
    return 0


def _linkedin_farm_status(args: argparse.Namespace) -> None:
    from .sources.account_farm import AccountFarm

    accounts = [a.strip() for a in args.accounts.split(",") if a.strip()]
    farm = AccountFarm(accounts=accounts)
    farm.print_farm_status()


async def _migrate(args: argparse.Namespace) -> int:
    from .migration.phase1 import migrate_phase1_data

    return await migrate_phase1_data(args.database)


async def _seed(args: argparse.Namespace) -> int:
    from .seed import run_seed

    return await run_seed(args)


if __name__ == "__main__":
    main()
