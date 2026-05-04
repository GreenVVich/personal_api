from importlib import import_module
from pathlib import Path

from app.box.runtime import action


def load_tools() -> None:
    base_path = Path(__file__).resolve().parent

    for module_path in sorted(base_path.glob("*.py")):
        if module_path.stem == "__init__":
            continue
        import_module(f"{__name__}.{module_path.stem}")


__all__ = ["action", "load_tools"]
