from typing import Any

from pydantic import BaseModel, Field, model_validator


class CalculatorInput(BaseModel):
    id: str
    required: bool = True
    default: float | None = None


class CalculatorConstant(BaseModel):
    id: str
    value: float


class CalculatorValueAction(BaseModel):
    id: str
    function: str
    args: dict[str, Any] | list[Any] | None = None


class CalculatorValue(BaseModel):
    id: str
    actions: list[CalculatorValueAction] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    text_template: str | None = None


class CalculatorDefinition(BaseModel):
    id: str
    inputs: list[CalculatorInput] = Field(default_factory=list)
    constants: list[CalculatorConstant] = Field(default_factory=list)
    values: list[CalculatorValue] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_graph(self) -> CalculatorDefinition:
        available: set[str] = {item.id for item in self.inputs}
        errors: list[str] = []

        for constant in self.constants:
            if constant.id in available:
                errors.append(f"duplicate '{constant.id}'")
            available.add(constant.id)

        for value in self.values:
            if not value.actions:
                errors.append(f"{value.id}: actions are required")
                continue

            for action in value.actions:
                sources: list[Any] = []
                if isinstance(action.args, list):
                    sources = action.args
                elif isinstance(action.args, dict):
                    sources = list(action.args.values())

                for source in sources:
                    if isinstance(source, str) and source not in available:
                        errors.append(f"{action.id}: missing '{source}'")

                available.add(action.id)

            available.add(value.id)

        if errors:
            raise ValueError(f"Dependency error: {errors}")

        return self


class CalculationRunRequest(BaseModel):
    inputs: dict[str, Any] = Field(default_factory=dict)
