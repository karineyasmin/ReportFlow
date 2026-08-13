from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from app.core.config import settings
from app.core.logger import logger


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


@app.get("/")
def read_root():
    """Root endpoint to check API health status."""
    logger.info("Root endpoint '/' accessed successfully.")
    return {"status": "ok", "project": settings.PROJECT_NAME}


@app.get("/api/v1/protected")
def protected_route(payload: Dict[str, Any] = Depends(require_role("report_admin"))):
    """Protected endpoint requiring the 'report_admin' Keycloak role."""
    user_name = payload.get("preferred_username", "Unknown")
    return {
        "message": f"Hello, {user_name}! You have access to this protected route.",
        "user_info": {
            "id": payload.get("sub"),
            "email": payload.get("email"),
            "roles": payload.get("realm_access", {}).get("roles", []),
        },
    }
