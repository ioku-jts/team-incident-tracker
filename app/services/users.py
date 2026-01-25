from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate


class UserService:
    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: UUID) -> User | None:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def list(db: AsyncSession) -> list[User]:
        result = await db.execute(select(User))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, user_in: UserCreate) -> User:
        user = User(**user_in.model_dump())
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
