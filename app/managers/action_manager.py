from typing import Any

from app.modules.calculations.service import CalculationService
from app.tools.action import get_action_handler, register_action_handlers, run_action_handler


class ActionError(Exception):
    pass


class ActionManager:
    def __init__(self, calculation_service: CalculationService | None = None) -> None:
        self.calculation_service: CalculationService = calculation_service or CalculationService()
        register_action_handlers(self.calculation_service)

    def run(
        self,
        group: str,
        action_id: str,
        input_data: dict[str, Any],
    ) -> Any:
        try:
            handler = get_action_handler(group, action_id)
            return run_action_handler(handler, input_data)
        except Exception as exc:
            raise ActionError(str(exc)) from exc


action_manager = ActionManager()
