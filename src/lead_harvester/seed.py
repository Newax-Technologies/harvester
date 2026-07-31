import argparse
import random
import sys
from uuid import uuid4

from sqlalchemy import text

from lead_harvester.config import settings
from lead_harvester.database import get_session
from lead_harvester.models.canonical import Branch, CanonicalInstitution, ContactPoint
from lead_harvester.models.outreach import AccountBrief, DraftStatus, OutreachDraft
from lead_harvester.models.research import FindingType, JobStatus, ResearchFinding, ResearchJob
from lead_harvester.models.resolution import MatchAssessment, MatchDecision, ResolutionCandidate
from lead_harvester.models.source import RawSourceRecord, RunStatus, SourceRun, SourceType


def generate_deterministic_uuid(seed: int, index: int) -> str:
    random.seed(f"{seed}-{index}")
    return str(uuid4())


async def run_seed(args: argparse.Namespace) -> int:
    if settings.app_env.lower() == "production" and not settings.allow_demo_seed:
        print(
            "Error: Seeding is not allowed in production unless ALLOW_DEMO_SEED=true.",
            file=sys.stderr,
        )
        return 1

    random.seed(args.seed)

    async with get_session() as session:
        if args.reset:
            print("Resetting demo data...")
            # Truncate tables for fresh seed
            await session.execute(text("TRUNCATE TABLE audit_logs CASCADE"))
            await session.execute(text("TRUNCATE TABLE resolution_candidates CASCADE"))
            await session.execute(text("TRUNCATE TABLE raw_source_records CASCADE"))
            await session.execute(text("TRUNCATE TABLE source_runs CASCADE"))
            await session.execute(text("TRUNCATE TABLE outreach_drafts CASCADE"))
            await session.execute(text("TRUNCATE TABLE research_findings CASCADE"))
            await session.execute(text("TRUNCATE TABLE contact_points CASCADE"))
            await session.execute(text("TRUNCATE TABLE branches CASCADE"))
            await session.execute(text("TRUNCATE TABLE canonical_institutions CASCADE"))

        institutions = []

        # Create Canonical Institutions
        for i in range(5):
            inst = CanonicalInstitution(
                canonical_name=f"Demo Institution {i}",
                domain=f"demo{i}.edu.pk",
                confidence_score=random.randint(60, 99),
            )
            session.add(inst)
            institutions.append(inst)

        await session.flush()

        # Branches and Contacts
        for inst in institutions:
            branch = Branch(
                institution_id=inst.id,
                branch_name="Main Campus",
                address=f"{random.randint(1, 100)} Main St",
                city="Karachi",
                country_code="PK",
                provider_ids={"google_place_id": f"ChIJ{random.randint(1000, 9999)}"},
            )
            session.add(branch)

            contact = ContactPoint(
                institution_id=inst.id,
                contact_type="email",
                contact_value=f"info@{inst.domain}",
                role="Admissions",
            )
            session.add(contact)

            job = ResearchJob(
                institution_id=inst.id, status=JobStatus.COMPLETED, objectives=["find_lms"]
            )
            session.add(job)
            await session.flush()

            # Add some findings
            finding = ResearchFinding(
                institution_id=inst.id,
                job_id=job.id,
                finding_type=FindingType.FACT,
                finding_key="software_usage",
                finding_value="Uses generic LMS",
                confidence_score=random.randint(50, 95),
            )
            session.add(finding)

        await session.flush()

        # Pending Drafts
        for i, inst in enumerate(institutions[:3]):
            brief = AccountBrief(institution_id=inst.id)
            session.add(brief)
            await session.flush()

            draft = OutreachDraft(
                brief_id=brief.id,
                target_name=f"Principal {i}",
                target_role="Principal",
                target_contact_value=f"principal{i}@{inst.domain}",
                subject_line=f"Upgrade your tech stack at {inst.canonical_name}",
                body=f"Hi Principal {i},\nWe saw your site {inst.domain} uses a basic LMS...",
                status=DraftStatus.GENERATED,
                version=1,
            )
            session.add(draft)

        # Resolution Candidates -- a demo "pending" candidate awaiting human
        # review via the actual schema: a candidate pairs a raw_record_id
        # (NOT NULL) with a target (target_canonical_id here) and a
        # blocking_strategy; scores/decision live on a separate
        # MatchAssessment row, not on the candidate itself.
        demo_run = SourceRun(
            source_type=SourceType.WEBSITE, run_metadata={}, status=RunStatus.COMPLETED
        )
        session.add(demo_run)
        await session.flush()

        incoming_name = f"Demo Inst {institutions[0].canonical_name}"
        incoming_record = RawSourceRecord(
            source_run_id=demo_run.id,
            source_type=SourceType.WEBSITE,
            source_id="https://external-demo-duplicate.example.edu",
            raw_payload={"name": incoming_name},
            normalized_name=incoming_name.lower(),
        )
        session.add(incoming_record)
        await session.flush()

        res_cand = ResolutionCandidate(
            raw_record_id=incoming_record.id,
            target_canonical_id=institutions[0].id,
            blocking_strategy="name_similarity",
            version=1,
        )
        session.add(res_cand)
        await session.flush()

        session.add(
            MatchAssessment(
                candidate_id=res_cand.id,
                name_similarity=0.75,
                total_score=75,
                decision=MatchDecision.PENDING,
            )
        )

        await session.flush()

    print("Seeding complete.")
    return 0
