from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.base import Base
from typing import List
from datetime import datetime

from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.models.organization import Organization
from app.models.membership import OrganizationMember
from app.schemas.membership import MembershipCreate, MembershipRead

router = APIRouter(prefix="/orgs/{org_id}/members", tags=["memberships"])

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/", response_model=List[MembershipRead])
async def get_org_members(org_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(OrganizationMember).where(OrganizationMember.organization_id == org_id)
    )
    return result.scalars().all()

@router.post("/", response_model=MembershipRead)
async def add_member(org_id: str, membership_in: MembershipCreate, db: AsyncSession = Depends(get_db)):
    # Ensure org exists
    org = await db.get(Organization, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    # Ensure user exists
    user = await db.get(User, membership_in.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_membership = OrganizationMember(
        user_id=user.id,
        organization_id=org.id,
        role=membership_in.role,
        created_at=datetime.utcnow()
    )
    db.add(new_membership)
    await db.commit()
    await db.refresh(new_membership)
    return new_membership
