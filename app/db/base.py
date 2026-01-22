from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Import models so Alembic can discover them
from app.models.user import User  # noqa
from app.models.organization import Organization  # noqa
from app.models.membership import OrganizationMember  # noqa