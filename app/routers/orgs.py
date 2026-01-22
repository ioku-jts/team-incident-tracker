from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.base import Base
from typing import List
from datetime import datetime

from app.db.session import AsyncSessionLocal
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationRead

router = APIRouter(prefix="/orgs", tags=["organizations"])

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/", response_model=List[OrganizationRead])
async def get_orgs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Organization))
    return result.scalars().all()

@router.get("/{org_id}", response_model=OrganizationRead)
async def get_org(org_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    org = result.scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.post("/", response_model=OrganizationRead)
async def create_org(org_in: OrganizationCreate, db: AsyncSession = Depends(get_db)):
    new_org = Organization(
        name=org_in.name,
        shortname=org_in.shortname,
        created_at=datetime.utcnow()
    )
    db.add(new_org)
    await db.commit()
    await db.refresh(new_org)
    return new_org
