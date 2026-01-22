from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MembershipBase(BaseModel):
    role: str


class MembershipCreate(MembershipBase):
    user_id: UUID
    organization_id: UUID


class MembershipRead(MembershipBase):
    id: UUID
    user_id: UUID
    organization_id: UUID
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
