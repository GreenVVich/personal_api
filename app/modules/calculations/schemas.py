from typing import Any

from pydantic import BaseModel, Field, model_validator


class SInput(BaseModel):
    id: str
    required: bool = True
    default: float | None = None


class SConstant(BaseModel):
    id: str
    value: float


class SValueAction(BaseModel):
    id: str
    function: str
    args: dict[str, Any] | list[Any] | None = None


class SValue(BaseModel):
    id: str
    actions: list[SValueAction] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    text_template: str | None = None


class SCalculator(BaseModel):
    id: str
    inputs: list[SInput] = Field(default_factory=list)
    constants: list[SConstant] = Field(default_factory=list)
    values: list[SValue] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_graph(self):
        available: set[str] = {input_def.id for input_def in self.inputs}
        errors: list[str] = []

        constant_ids: list[str] = [constant.id for constant in self.constants]
        duplicate_constants: set[str] = {
            constant_id for constant_id in constant_ids if constant_ids.count(constant_id) > 1
        }
        if duplicate_constants:
            raise ValueError(f"Duplicate constant ids: {sorted(duplicate_constants)}")

        for constant in self.constants:
            available.add(constant.id)

        for value in self.values:
            if not value.actions:
                errors.append(f"{value.id}: actions are required")
                continue

            for action in value.actions:
                if action.args is None:
                    available.add(action.id)
                    continue

                if isinstance(action.args, dict):
                    sources: list[Any] = list(action.args.values())
                else:
                    sources = list(action.args)

                for source in sources:
                    if isinstance(source, str) and source not in available:
                        errors.append(f"{action.id}: missing '{source}'")

                available.add(action.id)

            available.add(value.id)

        if errors:
            raise ValueError(f"Dependency error: {errors}")

        return self


class SCalcRequest(BaseModel):
    calculator_type: str
    inputs: dict[str, Any]
