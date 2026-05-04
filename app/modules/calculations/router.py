from fastapi import APIRouter, HTTPException

from app.box.repository import box_repository
from app.modules.calculations.schemas import CalculationRunRequest

router = APIRouter(prefix="/calculations", tags=["calculations"])


@router.get("/")
async def list_calculators() -> list[dict[str, object]]:
    return [
        {
            "name": box.name,
            "actions": list(box.actions),
        }
        for box in box_repository.list()
        if "calculate" in box.actions
    ]


@router.post("/{calculator_name}/run")
async def run_calculation(calculator_name: str, request: CalculationRunRequest) -> dict[str, object]:
    try:
        result = box_repository.run_action(calculator_name, "calculate", {"inputs": request.inputs})
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not isinstance(result, dict):
        raise HTTPException(status_code=500, detail="Calculation action returned unexpected result")
    return result
