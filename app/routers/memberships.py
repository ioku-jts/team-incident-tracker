from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.db.session import get_db
from app.schemas.membership import MembershipCreate, MembershipRead
from app.services.memberships import MembershipService

router = APIRouter(prefix="/memberships", tags=["memberships"])


@router.get("", response_model=List[MembershipRead])
async def list_memberships(
    organization_id: Optional[UUID] = None,
    user_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
):
    return await MembershipService.get_memberships(
        db=db,
        organization_id=organization_id,
        user_id=user_id,
    )

@router.post("/", response_model=MembershipRead, status_code=status.HTTP_201_CREATED)
async def add_member(
    payload: MembershipCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        membership = await MembershipService.add_member(
            db=db,
            organization_shortname=payload.organization_shortname,
            user_email=payload.email,
            role=payload.role,
        )
        return membership
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
