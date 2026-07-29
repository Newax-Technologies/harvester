from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.outreach import DraftStatus, OutreachDraft
from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.resolution import MatchAssessment, MatchDecision, ResolutionCandidate


class DashboardService:
    @staticmethod
    async def get_summary(session: AsyncSession) -> dict:
        total_institutions = await session.scalar(select(func.count(CanonicalInstitution.id)))
        pending_drafts = await session.scalar(
            select(func.count(OutreachDraft.id)).where(
                OutreachDraft.status == DraftStatus.GENERATED
            )
        )
        # Must match services/resolution_service.py::list_pending's filter --
        # otherwise this counted every ResolutionCandidate ever created
        # (including automated MERGE/LINK_ONLY/REJECT ones and already
        # human-reviewed ones), so the badge only ever grew and disagreed
        # with what the review queue actually shows.
        already_canonicalized = (
            select(FieldProvenance.raw_record_id)
            .where(FieldProvenance.raw_record_id == ResolutionCandidate.raw_record_id)
            .exists()
        )
        pending_resolutions = await session.scalar(
            select(func.count(ResolutionCandidate.id))
            .join(MatchAssessment, MatchAssessment.candidate_id == ResolutionCandidate.id)
            .where(
                MatchAssessment.decision == MatchDecision.PENDING,
                ResolutionCandidate.review_outcome.is_(None),
                # A sibling candidate for the same raw record may already
                # have been decided (or automated resolution already
                # canonicalized it entirely) -- without this exclusion the
                # badge kept counting a candidate that list_pending had
                # already dropped from the actual queue.
                ~already_canonicalized,
            )
        )

        return {
            "total_canonical_institutions": total_institutions or 0,
            "pending_resolution_candidates": pending_resolutions or 0,
            "pending_outreach_drafts": pending_drafts or 0,
            "total_target_accounts": total_institutions or 0,
            "recent_pipeline_activity": [],
        }
