import argparse
import random
import sys
from uuid import uuid4

from sqlalchemy import text

from lead_harvester.config import settings
from lead_harvester.database import get_session_factory
from lead_harvester.models.canonical import Branch, CanonicalInstitution, ContactPoint
from lead_harvester.models.outreach import AccountBrief, DraftStatus, OutreachDraft
from lead_harvester.models.research import FindingType, JobStatus, ResearchFinding, ResearchJob
from lead_harvester.models.resolution import ResolutionCandidate


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

    SessionLocal = get_session_factory()

    async with SessionLocal() as session, session.begin():
        if args.reset:
            print("Resetting demo data...")
            # Truncate tables for fresh seed
            await session.execute(text("TRUNCATE TABLE audit_logs CASCADE"))
            await session.execute(text("TRUNCATE TABLE resolution_candidates CASCADE"))
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

        # Resolution Candidates
        res_cand = ResolutionCandidate(
            target_institution_id=institutions[0].id,
            incoming_source_id="external_123",
            incoming_data={"name": f"Demo Inst {institutions[0].canonical_name}"},
            confidence_score=75,
            version=1,
        )
        session.add(res_cand)

        await session.flush()

    print("Seeding complete.")
    return 0
