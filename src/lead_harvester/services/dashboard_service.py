from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.outreach import DraftStatus, OutreachDraft
from lead_harvester.models.resolution import ResolutionCandidate


class DashboardService:
    @staticmethod
    async def get_summary(session: AsyncSession) -> dict:
        total_institutions = await session.scalar(select(func.count(CanonicalInstitution.id)))
        pending_drafts = await session.scalar(
            select(func.count(OutreachDraft.id)).where(
                OutreachDraft.status == DraftStatus.GENERATED
            )
        )
        pending_resolutions = await session.scalar(select(func.count(ResolutionCandidate.id)))

        return {
            "total_canonical_institutions": total_institutions or 0,
            "pending_resolution_candidates": pending_resolutions or 0,
            "pending_outreach_drafts": pending_drafts or 0,
            "total_target_accounts": total_institutions or 0,
            "recent_pipeline_activity": [],
        }
