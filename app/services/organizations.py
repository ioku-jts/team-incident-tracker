from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate


class OrganizationService:
    @staticmethod
    async def get_by_id(db: AsyncSession, org_id: UUID) -> Organization | None:
        result = await db.execute(
            select(Organization).where(Organization.id == org_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def list(db: AsyncSession) -> list[Organization]:
        result = await db.execute(select(Organization))
        return result.scalars().all()

    @staticmethod
    async def create(
        db: AsyncSession, org_in: OrganizationCreate
    ) -> Organization:
        org = Organization(**org_in.model_dump())
        db.add(org)
        await db.commit()
        await db.refresh(org)
        return org
