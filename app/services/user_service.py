import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repo import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    async def create_user(self, db: AsyncSession, name: str, email: str):
        logger.info(f"Creating user {name} with email {email}")
        user = User(
            name=name.strip().title(),  # business logic
            email=email.lower(),
        )
        return await self.repo.create(db, user)

    async def list_users(self, db: AsyncSession):
        logger.info("Listing users")

        users = await self.repo.fetch_all(db, limit=100)

        # Derived / CPU work (important for load test)
        return [{"id": u.id, "name": u.name, "email": u.email, "name_length": len(u.name)} for u in users]  # ty:ignore[invalid-argument-type]
