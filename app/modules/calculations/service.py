from __future__ import annotations

from typing import Any

from app.box.core import Box
from app.box.runtime import action
from app.modules.calculations.schemas import CalculatorDefinition, CalculatorValueAction


class CalculationError(Exception):
    pass


class CalculationService:
    def get_definition(self, box: Box) -> CalculatorDefinition:
        try:
            payload = {
                "id": box.name,
                "inputs": box.cells.get("inputs", []),
                "constants": box.cells.get("constants", []),
                "values": box.cells.get("values", []),
            }
            return CalculatorDefinition.model_validate(payload)
        except Exception as exc:
            raise CalculationError(f"Invalid calculator box '{box.name}': {exc}") from exc

    def validate_inputs(
        self,
        definition: CalculatorDefinition,
        data: dict[str, Any],
    ) -> dict[str, float]:
        context: dict[str, float] = {}
        missing: list[str] = []

        for input_def in definition.inputs:
            if input_def.id in data:
                context[input_def.id] = self._as_number(data[input_def.id], name=input_def.id)
            elif input_def.default is not None:
                context[input_def.id] = input_def.default
            elif input_def.required:
                missing.append(input_def.id)

        if missing:
            raise CalculationError(f"Missing inputs: {missing}")

        return context

    def resolve_action_args(
        self,
        action_def: CalculatorValueAction,
        context: dict[str, float],
    ) -> tuple[list[Any], dict[str, Any]]:
        if action_def.args is None:
            return [], {}

        if isinstance(action_def.args, list):
            return [self.resolve_value(item, context) for item in action_def.args], {}

        if isinstance(action_def.args, dict):
            return [], {key: self.resolve_value(value, context) for key, value in action_def.args.items()}

        raise CalculationError(f"{action_def.id}: unsupported args type")

    def resolve_value(self, value: Any, context: dict[str, float]) -> Any:
        if isinstance(value, str) and value in context:
            return context[value]
        return value

    def run_function(self, function_name: str, *args: Any, **kwargs: Any) -> float:
        from app.box.runtime import get_action_handler

        handler = get_action_handler(function_name)

        try:
            result = handler(*args, **kwargs)
        except Exception as exc:
            raise CalculationError(f"{function_name}: {exc}") from exc

        if not isinstance(result, int | float):
            raise CalculationError(f"{function_name}: result must be numeric, got {type(result).__name__}")

        return float(result)

    def execute_value(
        self,
        action_defs: list[CalculatorValueAction],
        context: dict[str, float],
    ) -> float:
        result: float | None = None

        for action_def in action_defs:
            args, kwargs = self.resolve_action_args(action_def, context)
            result = self.run_function(action_def.function, *args, **kwargs)
            context[action_def.id] = result

        if result is None:
            raise CalculationError("Value must contain at least one action")

        return result

    def calculate(self, box: Box, inputs: dict[str, Any]) -> dict[str, Any]:
        definition = self.get_definition(box)
        context = self.validate_inputs(definition, inputs)

        for constant in definition.constants:
            context[constant.id] = constant.value

        results: dict[str, float] = {}
        text_blocks: list[str] = []

        for value_def in definition.values:
            result = self.execute_value(value_def.actions, context)
            context[value_def.id] = result
            results[value_def.id] = result

            if "Show" in value_def.tags and value_def.text_template:
                text_blocks.append(value_def.text_template.format(**context))

        return {
            "calculator": definition.id,
            "results": results,
            "text": "\n".join(text_blocks),
        }

    @staticmethod
    def _as_number(value: Any, *, name: str) -> float:
        if not isinstance(value, int | float):
            raise CalculationError(f"{name} must be numeric")
        return float(value)


calculation_service = CalculationService()


@action("calculator.calculate", enable_logging=True)
def calculate_box(box: Box, inputs: dict[str, Any]) -> dict[str, Any]:
    return calculation_service.calculate(box, inputs)
