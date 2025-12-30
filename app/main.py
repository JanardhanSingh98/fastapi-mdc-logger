import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.logging import setup_logging
from app.middlewares.mdc_middleware import MDCMiddleware
from app.middlewares.profiler_middleware import ProfilerMiddleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    logger.info("Application started")
    yield
    # Shutdown
    logger.info("Application shutting down")


app = FastAPI(title="FastAPI MDC Logger", lifespan=lifespan)

app.add_middleware(MDCMiddleware)
app.add_middleware(ProfilerMiddleware)
app.include_router(health_router)
