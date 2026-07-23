from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from lead_harvester.api.dependencies import get_db_session, get_current_user, User
from lead_harvester.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=Dict[str, Any])
async def get_dashboard_summary(
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """Returns key metrics for the Command Center."""
    return await DashboardService.get_summary(session)

@router.get("/activity")
async def get_dashboard_activity(
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """Returns a timeline of recent pipeline activity."""
    # MOCK implementation
    return [
        {"id": 1, "type": "qualified", "message": "Qualified 5 new institutions", "timestamp": "2026-07-23T08:00:00Z"},
        {"id": 2, "type": "draft_approved", "message": "Approved draft for Principal at Example School", "timestamp": "2026-07-23T08:15:00Z"}
    ]
