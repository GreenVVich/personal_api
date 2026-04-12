from fastapi import APIRouter

from app.managers.action_manager import action_manager
from app.modules.calculations.schemas import SCalcRequest

router = APIRouter(prefix="/calculations")


@router.post("/")
async def run(request: SCalcRequest):
    return action_manager.run(
        group="calculations",
        action_id="calculate",
        input_data={
            "calculator_id": request.calculator_type,
            "inputs": request.inputs,
        },
    )
