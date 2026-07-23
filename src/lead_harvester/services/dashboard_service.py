from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.outreach import OutreachDraft, DraftStatus
from lead_harvester.models.resolution import ResolutionCandidate

class DashboardService:
    @staticmethod
    async def get_summary(session: AsyncSession) -> dict:
        total_institutions = await session.scalar(select(func.count(CanonicalInstitution.id)))
        pending_drafts = await session.scalar(
            select(func.count(OutreachDraft.id)).where(OutreachDraft.status == DraftStatus.READY_FOR_REVIEW)
        )
        pending_resolutions = await session.scalar(select(func.count(ResolutionCandidate.id)))
        
        return {
            "canonical_institutions": total_institutions or 0,
            "qualified_candidates": total_institutions or 0, # MOCK
            "pending_resolution_reviews": pending_resolutions or 0,
            "pending_outreach_drafts": pending_drafts or 0,
            "approved_drafts": 0,
            "rejected_drafts": 0,
            "meetings_booked": 0,
            "recent_pipeline_activity": []
        }
