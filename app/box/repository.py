from __future__ import annotations

from typing import Any

from app.box.core import Box
from app.box.runtime import execute_action


class BoxRepository:
    def __init__(self) -> None:
        self._boxes: dict[str, Box] = {}

    def register(self, box: Box) -> Box:
        box.validate()
        self._boxes[box.name] = box
        return box

    def get(self, name: str) -> Box:
        try:
            return self._boxes[name]
        except KeyError as exc:
            raise KeyError(f"Box '{name}' not found") from exc

    def list(self) -> list[Box]:
        return list(self._boxes.values())

    def export(self, name: str) -> dict[str, Any]:
        return self.get(name).to_dict()

    def import_box(self, payload: dict[str, Any]) -> Box:
        box = Box.from_dict(payload)
        return self.register(box)

    def run_action(self, name: str, action_name: str, input_data: dict[str, Any] | None = None) -> Any:
        box = self.get(name)
        return execute_action(box, action_name, input_data=input_data, repository=self)


box_repository = BoxRepository()
