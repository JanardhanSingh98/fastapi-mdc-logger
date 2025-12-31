from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    async def create(self, db: AsyncSession, user: User) -> User:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def fetch_all(self, db: AsyncSession, limit: int = 100) -> list[User]:
        result = await db.execute(select(User).limit(limit))
        return result.scalars().all()  # ty:ignore[invalid-return-type]
