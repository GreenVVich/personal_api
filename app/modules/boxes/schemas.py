from typing import Any

from pydantic import BaseModel, Field


class BoxPayload(BaseModel):
    name: str
    cells: dict[str, Any] = Field(default_factory=dict)
    actions: dict[str, dict[str, Any]] = Field(default_factory=dict)


class BoxActionRunRequest(BaseModel):
    input_data: dict[str, Any] = Field(default_factory=dict)
