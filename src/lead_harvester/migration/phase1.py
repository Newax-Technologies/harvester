import json

from lead_harvester.database import get_session
from lead_harvester.models import RawSourceRecord, RunStatus, SourceRun, SourceType
from lead_harvester.storage.sqlite import SQLiteStore


async def migrate_phase1_data(database_path: str) -> None:
    print(f"Connecting to SQLite database at {database_path}...")
    store = SQLiteStore(database_path)

    # Check if there are any institutions
    cursor = store.connection.execute("SELECT id, raw_data FROM institutions")
    rows = cursor.fetchall()

    if not rows:
        print("No Phase 1 data found. Migration complete.")
        store.close()
        return

    print(f"Found {len(rows)} Phase 1 records to migrate.")

    async with get_session() as session:
        # Create a single SourceRun for this migration
        run = SourceRun(
            source_type=SourceType.MANUAL,
            run_metadata={"description": "Phase 1 Migration from SQLite"},
            status=RunStatus.COMPLETED,
        )
        session.add(run)
        await session.flush()

        migrated_count = 0
        for row in rows:
            inst_id = row["id"]
            raw_data_str = row["raw_data"]

            try:
                raw_payload = json.loads(raw_data_str) if raw_data_str else {}
            except json.JSONDecodeError:
                print(f"Warning: Failed to parse raw_data for {inst_id}. Skipping.")
                continue

            # If the raw data is empty, we don't have the original payload.
            if not raw_payload:
                continue

            # Usually Phase 1 was Google Places, but we mark as MANUAL migration if unsure.
            # We can infer source_id from place_id if present.
            source_id = raw_payload.get("id", inst_id)

            record = RawSourceRecord(
                source_run_id=run.id,
                source_type=SourceType.GOOGLE_PLACES
                if "google" in str(raw_payload).lower() or "displayName" in raw_payload
                else SourceType.MANUAL,
                source_id=source_id,
                raw_payload=raw_payload,
            )
            session.add(record)
            migrated_count += 1

        print(f"Successfully migrated {migrated_count} records into the Source Ledger.")

    store.close()
