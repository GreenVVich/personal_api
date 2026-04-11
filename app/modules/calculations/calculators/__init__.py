from importlib import import_module
from pathlib import Path

from app.modules.calculations.schemas import SCalculator


def load_calculators() -> list[SCalculator]:
    calculators: list[SCalculator] = []
    base_path = Path(__file__).resolve().parent

    for module_path in sorted(base_path.glob("*.py")):
        if module_path.stem == "__init__":
            continue

        module = import_module(f"{__name__}.{module_path.stem}")
        calculator = getattr(module, "calculator", None)
        if calculator is None:
            continue

        if not isinstance(calculator, SCalculator):
            raise TypeError(
                f"{module.__name__}.calculator must be an instance of SCalculator"
            )

        calculators.append(calculator)

    return calculators
