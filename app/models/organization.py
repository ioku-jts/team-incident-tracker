from sqlalchemy import String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin, SoftDeleteMixin

class Organization(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "organizations"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    name = mapped_column(
        String(255),
        nullable=False,
    )

    shortname = mapped_column(
        String(15),
        nullable=False,
        unique=True,
        index=True,
    )

    members = relationship(
        "OrganizationMember",
        back_populates="organization",
        lazy="selectin",
    )
