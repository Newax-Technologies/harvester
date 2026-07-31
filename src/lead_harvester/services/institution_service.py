from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.schemas.institutions import InstitutionListResponse, PaginatedInstitutions


class InstitutionService:
    @staticmethod
    async def get_institutions(
        session: AsyncSession, limit: int = 50, offset: int = 0, city: str | None = None
    ) -> PaginatedInstitutions:
        query = select(CanonicalInstitution).order_by(CanonicalInstitution.created_at.desc())

        # MOCK filter logic for city (would typically join with Branch)

        total = await session.scalar(select(func.count()).select_from(query.subquery()))

        query = query.offset(offset).limit(limit)
        result = await session.execute(query)
        institutions = result.scalars().all()

        items = [InstitutionListResponse.model_validate(inst) for inst in institutions]

        return PaginatedInstitutions(
            items=items, total=total or 0, page=(offset // limit) + 1 if limit else 1, size=limit
        )

    @staticmethod
    async def get_institution_detail(
        session: AsyncSession, institution_id: str
    ) -> CanonicalInstitution | None:
        query = (
            select(CanonicalInstitution)
            .options(
                selectinload(CanonicalInstitution.branches),
                selectinload(CanonicalInstitution.contact_points),  # Fixed relationship name
            )
            .where(CanonicalInstitution.id == institution_id)
        )

        result = await session.execute(query)
        return result.scalars().first()
