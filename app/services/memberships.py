from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Optional

from app.models.organization import Organization
from app.models.user import User
from app.models.membership import OrganizationMember


class MembershipService:
    @staticmethod
    async def add_member(
        *,
        db: AsyncSession,
        organization_shortname: str,
        user_email: str,
        role: str,
    ) -> OrganizationMember:
        # Fetch organization
        org = (
            await db.execute(
                select(Organization).where(
                    Organization.shortname == organization_shortname,
                    Organization.deleted_at.is_(None),
                )
            )
        ).scalar_one_or_none()

        if not org:
            raise ValueError("Organization not found")

        # Fetch or create user
        user = (
            await db.execute(
                select(User).where(
                    User.email == user_email,
                    User.deleted_at.is_(None),
                )
            )
        ).scalar_one_or_none()

        if not user:
            user = User(
                email=user_email,
                created_at=datetime.utcnow(),
            )
            db.add(user)
            await db.flush()  # get user.id without commit

        # Check existing membership
        existing = (
            await db.execute(
                select(OrganizationMember).where(
                    OrganizationMember.user_id == user.id,
                    OrganizationMember.organization_id == org.id,
                    OrganizationMember.deleted_at.is_(None),
                )
            )
        ).scalar_one_or_none()

        if existing:
            raise ValueError("User is already a member of this organization")

        membership = OrganizationMember(
            user_id=user.id,
            organization_id=org.id,
            role=role,
            created_at=datetime.utcnow(),
        )

        db.add(membership)
        await db.commit()
        await db.refresh(membership)

        return membership

    @staticmethod
    async def get_memberships(
        db: AsyncSession,
        organization_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None,
    ) -> List[OrganizationMember]:
        stmt = select(OrganizationMember)

        if organization_id:
            stmt = stmt.where(OrganizationMember.organization_id == organization_id)

        if user_id:
            stmt = stmt.where(OrganizationMember.user_id == user_id)

        result = await db.execute(stmt)
        return result.scalars().all()