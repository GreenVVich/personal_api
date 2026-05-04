from fastapi import APIRouter, HTTPException

from app.box.repository import box_repository
from app.modules.boxes.schemas import BoxActionRunRequest, BoxPayload

router = APIRouter(prefix="/boxes", tags=["boxes"])


@router.get("/")
async def list_boxes() -> list[dict[str, object]]:
    return [
        {
            "name": box.name,
            "actions": list(box.actions),
            "cells": list(box.cells),
        }
        for box in box_repository.list()
    ]


@router.post("/import")
async def import_box(request: BoxPayload) -> dict[str, object]:
    try:
        box = box_repository.import_box(request.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return box.to_dict()


@router.get("/{box_name}")
async def export_box(box_name: str) -> dict[str, object]:
    try:
        return box_repository.export(box_name)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{box_name}/actions/{action_name}")
async def run_box_action(
    box_name: str,
    action_name: str,
    request: BoxActionRunRequest,
) -> object:
    try:
        return box_repository.run_action(box_name, action_name, request.input_data)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
