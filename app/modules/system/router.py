from fastapi import APIRouter, HTTPException

from app.box.repository import box_repository
from app.core.logging import get_logger

logger = get_logger("system")
router = APIRouter(tags=["system"])


@router.get("/health")
async def healthcheck() -> dict[str, str]:
    logger.info("Healthcheck requested")
    return {"status": "ok"}


@router.get("/system/box")
async def get_system_box() -> dict[str, object]:
    try:
        return box_repository.export("system")
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/system/refresh")
async def refresh_system_snapshot() -> object:
    try:
        return box_repository.run_action("system", "refresh_snapshot", {})
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/system/snapshot")
async def get_snapshot() -> object:
    try:
        return box_repository.run_action("system", "get_snapshot", {})
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/system/docker")
async def list_docker_containers() -> object:
    try:
        return box_repository.run_action("system", "list_docker_containers", {})
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/system/cmd")
async def run_system_command(command: dict[str, str]) -> object:
    try:
        return box_repository.run_action("system", "run_cmd", command)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
