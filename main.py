from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from app.core import settings
from app.core import logger
from app.api import reports_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles application startup and shutdown lifecycle events."""
    logger.info("==================================================")
    logger.info(f" Starting application: {settings.PROJECT_NAME}")
    logger.warning("This is a WARNING log to verify terminal color mapping.")
    logger.error("This is an ERROR log to verify terminal color mapping.")
    logger.info("==================================================")

    yield

    logger.info("==================================================")
    logger.info(f" Shutting down application: {settings.PROJECT_NAME}")
    logger.info("==================================================")


app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0", lifespan=lifespan)
app.include_router(reports_router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    """Public health endpoint."""
    return {"status": "ok", "project": settings.PROJECT_NAME}
