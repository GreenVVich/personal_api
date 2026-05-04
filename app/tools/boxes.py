from __future__ import annotations

from typing import Any

from app.box.core import Box
from app.box.repository import BoxRepository, box_repository
from app.box.runtime import action


@action("box.list")
def list_boxes(repository: BoxRepository | None = None) -> list[dict[str, Any]]:
    source = repository or box_repository
    return [
        {
            "name": box.name,
            "cells": list(box.cells),
            "actions": list(box.actions),
        }
        for box in source.list()
    ]


@action("box.export")
def export_box(name: str, repository: BoxRepository | None = None) -> dict[str, Any]:
    source = repository or box_repository
    return source.export(name)


@action("box.get_value")
def get_box_value(
    box_name: str | Box,
    key: str,
    *,
    repository: BoxRepository | None = None,
    default: Any = None,
) -> Any:
    source = repository or box_repository
    box = box_name if isinstance(box_name, Box) else source.get(box_name)
    return box.cells.get(key, default)


@action("box.set_value")
def set_box_value(
    box_name: str | Box,
    key: str,
    value: Any,
    *,
    repository: BoxRepository | None = None,
) -> dict[str, Any]:
    source = repository or box_repository
    box = box_name if isinstance(box_name, Box) else source.get(box_name)
    box.cells[key] = value
    box.validate()
    source.register(box)

    return {
        "box": box.name,
        "key": key,
        "value": value,
    }
