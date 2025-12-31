import logging
from contextlib import asynccontextmanager
from gc import enable

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.user import user_router
from app.core.database import close_db, init_db
from app.core.logging import setup_logging
from app.core.settings import get_settings
from app.middlewares.mdc_middleware import MDCMiddleware
from app.middlewares.profiler_middleware import ProfilerMiddleware

settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    init_db()
    logger.info("Application started")
    yield
    await close_db()
    logger.info("Application shutting down")


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

app.add_middleware(MDCMiddleware)  # ty:ignore[invalid-argument-type]
app.add_middleware(ProfilerMiddleware, enabled=settings.enable_profiler)  # ty:ignore[invalid-argument-type]
app.include_router(health_router)
app.include_router(user_router)
