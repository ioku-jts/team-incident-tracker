from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class OrganizationBase(BaseModel):
    name: str
    shortname: str


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationRead(OrganizationBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
