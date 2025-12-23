import logging

from fastapi import APIRouter

from app.services.health_service import health_check_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
async def health_check():
    logger.info("Health check endpoint called")
    await health_check_service()
    return {"status": "ok"}
