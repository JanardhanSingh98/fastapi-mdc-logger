import logging

logger = logging.getLogger(__name__)


async def health_check_service():
    logger.info("Health check service called")
