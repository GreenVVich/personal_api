from fastapi import APIRouter
from app.managers.calculator_manager import manager
from app.modules.calculations.schemas import CalcRequest

router = APIRouter(prefix="/calculations")

@router.post("/")
def run(request: CalcRequest):
    return manager.calculate(request.calculator_type, request.inputs)
