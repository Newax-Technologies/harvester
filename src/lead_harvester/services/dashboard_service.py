from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.outreach import OutreachDraft, DraftStatus
from lead_harvester.models.resolution import ResolutionCandidate
from lead_harvester.models.audit import AuditLog

ACTIVITY_TYPE_MAP = {
    "draft.approved": "draft_approved",
    "draft.rejected": "draft_rejected",
    "draft.edited": "draft_edited",
    "resolution.same_business": "resolution_merged",
    "resolution.same_branch": "resolution_linked",
    "resolution.keep_separate": "resolution_rejected",
}

ACTIVITY_MESSAGE_TEMPLATES = {
    "draft.approved": "Approved outreach draft {entity_id}",
    "draft.rejected": "Sent outreach draft {entity_id} back for revision",
    "draft.edited": "Edited outreach draft {entity_id}",
    "resolution.same_business": "Merged resolution candidate {entity_id} as the same business",
    "resolution.same_branch": "Linked resolution candidate {entity_id} as a related branch",
    "resolution.keep_separate": "Rejected resolution candidate {entity_id} as unrelated",
}


def _activity_message(log: AuditLog) -> str:
    template = ACTIVITY_MESSAGE_TEMPLATES.get(log.action)
    if template:
        return template.format(entity_id=log.entity_id)
    return f"{log.action} on {log.entity_type} {log.entity_id}"


class DashboardService:
    @staticmethod
    async def get_summary(session: AsyncSession) -> dict:
        total_institutions = await session.scalar(select(func.count(CanonicalInstitution.id)))
        pending_drafts = await session.scalar(
            select(func.count(OutreachDraft.id)).where(OutreachDraft.status == DraftStatus.GENERATED)
        )
        pending_resolutions = await session.scalar(select(func.count(ResolutionCandidate.id)))

        return {
            "total_canonical_institutions": total_institutions or 0,
            "pending_resolution_candidates": pending_resolutions or 0,
            "pending_outreach_drafts": pending_drafts or 0,
            "total_target_accounts": total_institutions or 0,
            "recent_pipeline_activity": await DashboardService.get_recent_activity(session, limit=10)
        }

    @staticmethod
    async def get_recent_activity(session: AsyncSession, limit: int = 20) -> list[dict]:
        stmt = select(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit)
        logs = (await session.execute(stmt)).scalars().all()

        return [
            {
                "id": str(log.id),
                "type": ACTIVITY_TYPE_MAP.get(log.action, log.action),
                "message": _activity_message(log),
                "timestamp": log.timestamp.isoformat(),
            }
            for log in logs
        ]
