import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.user_service import UserService

user_router = APIRouter(prefix="/users", tags=["users"])
service = UserService()

logger = logging.getLogger(__name__)


@user_router.post("/")
async def create_user(payload: dict, db: AsyncSession = Depends(get_db)):
    logger.info("Inside create_user api")
    return await service.create_user(db, payload["name"], payload["email"])


@user_router.get("/")
async def list_users(db: AsyncSession = Depends(get_db)):
    logger.info("Inside list_users api")
    return await service.list_users(db)
