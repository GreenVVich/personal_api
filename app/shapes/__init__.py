from importlib import import_module
from pathlib import Path

from app.box.core import Box


def load_calculator_boxes() -> list[Box]:
    boxes: list[Box] = []
    base_path = Path(__file__).resolve().parent

    for module_path in sorted(base_path.glob("*.py")):
        if module_path.stem == "__init__":
            continue

        module = import_module(f"{__name__}.{module_path.stem}")
        box = getattr(module, "box", None)
        if box is None:
            continue
        if not isinstance(box, Box):
            raise TypeError(f"{module.__name__}.box must be an instance of Box")
        boxes.append(box)

    return boxes
