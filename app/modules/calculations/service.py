from typing import Any

from app.modules.calculations.calculators import load_calculators_from_repo
from app.modules.calculations.schemas import SCalculator, SValue, SValueAction
from app.tools.action import action
from app.tools.registry import get


class CalculationError(Exception):
    pass


class CalculationService:
    calculators: list[SCalculator]

    def __init__(self) -> None:
        self.calculators = [*load_calculators_from_repo()]

    def get_calculator(self, calc_id: str) -> SCalculator:
        for calculator in self.calculators:
            if calculator.id == calc_id:
                return calculator
        raise CalculationError(f"Calculator '{calc_id}' not found")

    def validate_calculator(
        self,
        calculator: SCalculator,
        data: dict[str, float],
    ) -> dict[str, float]:
        context: dict[str, float] = {}
        missing_inputs: list[str] = []

        for input_def in calculator.inputs:
            if input_def.id in data:
                context[input_def.id] = data[input_def.id]
            elif input_def.default is not None:
                context[input_def.id] = input_def.default
            elif input_def.required:
                missing_inputs.append(input_def.id)

        if missing_inputs:
            raise CalculationError(f"Missing inputs: {missing_inputs}")

        return context

    def resolve_arg(self, source: Any, context: dict[str, float]) -> Any:
        if isinstance(source, str) and source in context:
            return context[source]
        return source

    def resolve_action_args(
        self,
        value_action: SValueAction,
        context: dict[str, float],
    ) -> tuple[list[Any], dict[str, Any]]:
        if value_action.args is None:
            return [], {}

        if isinstance(value_action.args, dict):
            return [], {param: self.resolve_arg(source, context) for param, source in value_action.args.items()}

        if isinstance(value_action.args, list):
            return [self.resolve_arg(source, context) for source in value_action.args], {}

        raise CalculationError(f"{value_action.id}: unsupported args type")

    def execute_action(
        self,
        value_action: SValueAction,
        context: dict[str, float],
    ) -> float:
        function = get(value_action.function)
        positional_args, keyword_args = self.resolve_action_args(value_action, context)

        try:
            result: object = function(*positional_args, **keyword_args)
        except Exception as exc:
            raise CalculationError(f"{value_action.function}: {exc}") from exc

        if not isinstance(result, int | float):
            raise CalculationError(f"{value_action.function}: result must be numeric, got {type(result).__name__}")

        return float(result)

    def execute_value(
        self,
        value_def: SValue,
        context: dict[str, float],
    ) -> float:
        result: float | None = None

        for value_action in value_def.actions:
            result = self.execute_action(value_action, context)
            context[value_action.id] = result

        if result is None:
            raise CalculationError(f"{value_def.id}: action result is required")

        context[value_def.id] = result
        return result

    @action("calculate", group="calculations", enable_logging=True)
    def calculate(
        self,
        calculator_id: str,
        inputs: dict[str, float],
    ) -> dict[str, str | dict[str, float]]:
        calculator: SCalculator = self.get_calculator(calculator_id)
        context: dict[str, float] = self.validate_calculator(calculator, inputs)

        for constant in calculator.constants:
            context[constant.id] = constant.value

        results: dict[str, float] = {}
        text_blocks: list[str] = []

        for value_def in calculator.values:
            value: float = self.execute_value(value_def, context)
            results[value_def.id] = value

            if "Show" in value_def.tags and value_def.text_template:
                text_blocks.append(value_def.text_template.format(**context))

        return {
            "calculator": calculator.id,
            "results": results,
            "text": "\n".join(text_blocks),
        }
