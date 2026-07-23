import asyncio
from sqlalchemy import select
from lead_harvester.database import get_session
from lead_harvester.models import RawSourceRecord
import json

async def main():
    async with get_session() as session:
        records = await session.scalars(
            select(RawSourceRecord)
            .where(RawSourceRecord.source_type == "website")
            .order_by(RawSourceRecord.extracted_at.desc())
            .limit(10)
        )
        
        print("\n=== RECENT LEADS EXTRACTED BY WEBCRAWLER ===")
        for r in records:
            print(f"\nSource ID (URL): {r.source_id}")
            print(f"Name: {r.normalized_name}")
            print(f"Phone: {r.normalized_phone}")
            print("Extracted Data:")
            print(json.dumps(r.raw_payload, indent=2))
            print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())
