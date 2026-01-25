from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.session import get_db
from app.schemas.organization import OrganizationRead, OrganizationCreate
from app.services.organizations import OrganizationService

router = APIRouter(prefix="/orgs", tags=["organizations"])


@router.get("/", response_model=list[OrganizationRead])
async def list_organizations(db: AsyncSession = Depends(get_db)):
    return await OrganizationService.list(db)


@router.post("/", response_model=OrganizationRead)
async def create_org(
    org_in: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
):
    return await OrganizationService.create(db, org_in)

@router.get("/{org_id}", response_model=OrganizationRead)
async def get_org(
    org_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    org = await OrganizationService.get_by_id(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org