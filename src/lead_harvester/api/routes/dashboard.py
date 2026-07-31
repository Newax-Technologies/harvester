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
    return await DashboardService.get_recent_activity(session)
