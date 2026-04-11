from pydantic import BaseModel, Field, model_validator
from typing import List, Dict, Optional, Any


class SInput(BaseModel):
    id: str
    required: bool = True
    default: Optional[float] = None


class SConstant(BaseModel):
    value: float


class SValue(BaseModel):
    id: str
    function: Optional[str] = None
    args: Dict[str, str] = Field(default_factory=dict)
    value: Optional[float] = None
    tags: List[str] = Field(default_factory=list)
    text_template: Optional[str] = None
    round: Optional[int] = None


class SCalculator(BaseModel):
    id: str
    inputs: List[SInput] = Field(default_factory=list)
    constants: Dict[str, SConstant]
    values: List[SValue] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_graph(self):
        available = set()

        # inputs
        for i in self.inputs:
            available.add(i.id)

        # constants
        for c in self.constants.keys():
            available.add(c)

        errors = []

        for v in self.values:
            if v.function:
                for source in v.args.values():
                    if source not in available:
                        errors.append(f"{v.id}: missing '{source}'\n")

            available.add(v.id)

        if errors:
            raise ValueError(f"Dependency error: {errors}")

        return self

class CalcRequest(BaseModel):
    calculator_type: str
    inputs: Dict[str, Any]
