from app.box.repository import box_repository
from app.modules.calculations.service import calculation_service
from app.shapes import load_calculator_boxes
from app.tools import load_tools

load_tools()

for calculator_box in load_calculator_boxes():
    box_repository.register(calculator_box)

__all__ = ["calculation_service"]
