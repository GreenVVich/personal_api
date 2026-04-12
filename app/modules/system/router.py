from fastapi import APIRouter

from app.core.logging import get_logger

logger = get_logger("system")
router = APIRouter(tags=["system"])


@router.get("/health")
async def healthcheck() -> dict[str, str]:
    logger.info("Healthcheck requested")
    return {"status": "ok"}
