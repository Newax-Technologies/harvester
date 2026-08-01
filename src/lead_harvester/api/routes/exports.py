import uuid

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.dependencies import get_db_session
from lead_harvester.api.permissions import Permission, require_permission
from lead_harvester.exports import build_lead_export_rows, rows_to_csv, rows_to_json
from lead_harvester.models.canonical import OperatingStatus
from lead_harvester.models.qualification import QualificationStatus

router = APIRouter(
    prefix="/exports",
    tags=["Exports"],
    dependencies=[Depends(require_permission(Permission.LEADS_EXPORT))],
)


@router.get("/leads")
async def export_leads_route(
    format: str = Query("csv", pattern="^(csv|json)$"),
    status: OperatingStatus | None = Query(None),
    min_score: int | None = Query(None, ge=0),
    qualification_status: QualificationStatus | None = Query(None),
    sector_id: uuid.UUID | None = Query(None),
    limit: int = Query(1000, ge=1, le=10000),
    session: AsyncSession = Depends(get_db_session),
):
    """
    One row per contact point across matching institutions, as a CSV or
    JSON download -- see exports/lead_export.py for row shape and the
    reasoning behind that granularity.
    """
    rows = await build_lead_export_rows(
        session,
        status=status,
        min_score=min_score,
        qualification_status=qualification_status,
        sector_id=sector_id,
        limit=limit,
    )
    if format == "json":
        return Response(
            content=rows_to_json(rows),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=leads.json"},
        )
    return Response(
        content=rows_to_csv(rows),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=leads.csv"},
    )
