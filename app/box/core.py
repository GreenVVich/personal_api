from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class BoxAction:
    handler: str
    args: dict[str, Any] | list[Any] | None = None
    description: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "handler": self.handler,
            "args": self.args,
        }
        if self.description is not None:
            data["description"] = self.description
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BoxAction:
        return cls(
            handler=str(data["handler"]),
            args=data.get("args"),
            description=data.get("description"),
        )


@dataclass(slots=True)
class Box:
    name: str
    cells: dict[str, Any] = field(default_factory=dict)
    actions: dict[str, BoxAction] = field(default_factory=dict)

    def validate(self) -> None:
        names: set[str] = set()
        self._collect_names(names)

    def _collect_names(self, names: set[str]) -> None:
        if self.name in names:
            raise ValueError(f"Duplicate box or cell name: '{self.name}'")
        names.add(self.name)

        for cell_name, cell_value in self.cells.items():
            if cell_name in names:
                raise ValueError(f"Duplicate box or cell name: '{cell_name}'")
            names.add(cell_name)

            if isinstance(cell_value, Box):
                cell_value._collect_names(names)

    def get_name_index(self) -> dict[str, Any]:
        index: dict[str, Any] = {}
        self._fill_name_index(index)
        return index

    def _fill_name_index(self, index: dict[str, Any]) -> None:
        index[self.name] = self
        for cell_name, cell_value in self.cells.items():
            index[cell_name] = cell_value
            if isinstance(cell_value, Box):
                cell_value._fill_name_index(index)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "cells": {name: self._serialize_value(value) for name, value in self.cells.items()},
            "actions": {name: action.to_dict() for name, action in self.actions.items()},
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Box:
        box = cls(
            name=str(data["name"]),
            cells={name: cls._deserialize_value(value) for name, value in data.get("cells", {}).items()},
            actions={name: BoxAction.from_dict(action_data) for name, action_data in data.get("actions", {}).items()},
        )
        box.validate()
        return box

    @classmethod
    def _serialize_value(cls, value: Any) -> Any:
        if isinstance(value, Box):
            return {"$box": value.to_dict()}
        if isinstance(value, list):
            return [cls._serialize_value(item) for item in value]
        if isinstance(value, dict):
            return {key: cls._serialize_value(item) for key, item in value.items()}
        return value

    @classmethod
    def _deserialize_value(cls, value: Any) -> Any:
        if isinstance(value, dict) and "$box" in value:
            return cls.from_dict(value["$box"])
        if isinstance(value, list):
            return [cls._deserialize_value(item) for item in value]
        if isinstance(value, dict):
            return {key: cls._deserialize_value(item) for key, item in value.items()}
        return value
