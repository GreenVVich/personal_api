from __future__ import annotations

from pathlib import Path
from typing import Any

from app.box.runtime import action


@action("file.create")
def create_file(path: str, content: str = "", *, overwrite: bool = False, encoding: str = "utf-8") -> dict[str, Any]:
    target = Path(path).expanduser()
    if target.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {target}")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding=encoding)

    return {
        "path": str(target),
        "size": target.stat().st_size,
        "created": True,
    }


@action("file.read")
def read_file(path: str, *, encoding: str = "utf-8") -> dict[str, Any]:
    target = Path(path).expanduser()
    content = target.read_text(encoding=encoding)

    return {
        "path": str(target),
        "content": content,
        "size": target.stat().st_size,
    }


@action("file.update_text")
def update_text_file(
    path: str,
    *,
    old: str,
    new: str,
    count: int = -1,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    target = Path(path).expanduser()
    content = target.read_text(encoding=encoding)
    updated = content.replace(old, new, count)
    if updated == content:
        return {
            "path": str(target),
            "changed": False,
            "replacements": 0,
        }

    target.write_text(updated, encoding=encoding)
    replacements = content.count(old) if count < 0 else min(content.count(old), count)
    return {
        "path": str(target),
        "changed": True,
        "replacements": replacements,
    }
