from importlib import import_module
from pathlib import Path


def load_functions() -> None:
    base_path = Path(__file__).resolve().parent

    for module_path in sorted(base_path.glob("*.py")):
        if module_path.stem == "__init__":
            continue

        import_module(f"{__name__}.{module_path.stem}")
