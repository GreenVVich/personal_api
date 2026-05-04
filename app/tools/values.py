from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any

from app.box.runtime import action


@action("value.get")
def get_value(source: dict[str, Any], path: str, *, default: Any = None, separator: str = ".") -> Any:
    current: Any = source
    for key in _path_parts(path, separator):
        if isinstance(current, dict) and key in current:
            current = current[key]
            continue
        return default
    return current


@action("value.set")
def set_value(source: dict[str, Any], path: str, value: Any, *, separator: str = ".") -> dict[str, Any]:
    target: MutableMapping[str, Any] = source
    parts = _path_parts(path, separator)
    if not parts:
        raise ValueError("path must not be empty")

    for key in parts[:-1]:
        existing = target.get(key)
        if not isinstance(existing, dict):
            existing = {}
            target[key] = existing
        target = existing

    target[parts[-1]] = value
    return source


@action("value.pick")
def pick_values(source: dict[str, Any], keys: list[str]) -> dict[str, Any]:
    return {key: source[key] for key in keys if key in source}


def _path_parts(path: str, separator: str) -> list[str]:
    return [part for part in path.split(separator) if part]
