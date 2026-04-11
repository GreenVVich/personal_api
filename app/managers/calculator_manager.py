from app.modules.calculations.calculators import load_calculators
from app.core.logging import logger
from app.tools.registry import get
from app.modules.calculations.schemas import SCalculator


class CalculatorError(Exception):
    pass


class CalculatorManager:

    def load_raw(self) -> list[SCalculator]:
        return load_calculators()

    def load(self) -> list[SCalculator]:
        return self.load_raw()

    def get(self, calc_id: str) -> SCalculator:
        for c in self.load():
            if c.id == calc_id:
                logger.info("Loaded calculator '%s'", calc_id)
                return c
        logger.error("Calculator '%s' not found", calc_id)
        raise CalculatorError(f"Calculator '{calc_id}' not found")

    def prepare_inputs(self, calc: SCalculator, data: dict[str, float]) -> dict[str, float]:
        ctx: dict[str, float] = {}
        missing: list[str] = []

        for i in calc.inputs:
            if i.id in data:
                ctx[i.id] = data[i.id]
            elif i.default is not None:
                ctx[i.id] = i.default
            elif i.required:
                missing.append(i.id)

        if missing:
            logger.warning("Missing inputs for calculator '%s': %s", calc.id, missing)
            raise CalculatorError(f"Missing inputs: {missing}")

        return ctx

    def calculate(self, calc_id: str, data: dict[str, float]) -> dict[str, str | dict[str, float]]:
        calc = self.get(calc_id)

        ctx: dict[str, float] = self.prepare_inputs(calc, data)

        # constants
        for k, v in calc.constants.items():
            ctx[k] = v.value

        results: dict[str, float] = {}
        text: list[str] = []

        for v in calc.values:

            if v.function:
                func = get(v.function)

                # mapping param -> source
                args: dict[str, float | None] = {
                    param: ctx.get(src) for param, src in v.args.items()
                }

                missing = [k for k, val in args.items() if val is None]
                if missing:
                    logger.warning("Missing calculated arguments for '%s': %s", v.id, missing)
                    raise CalculatorError(f"{v.id}: missing {missing}")

                try:
                    value = func(**args)
                except Exception as e:
                    logger.exception("Calculation step '%s' failed", v.id)
                    raise CalculatorError(f"{v.id}: {str(e)}")

            else:
                value = v.value

            if v.round is not None:
                value = round(value, v.round)

            ctx[v.id] = value
            results[v.id] = value

            if "Show" in v.tags and v.text_template:
                text.append(v.text_template.format(**ctx))

        logger.info("Calculator '%s' completed with results: %s", calc.id, results)

        return {
            "calculator": calc.id,
            "results": results,
            "text": "\n".join(text)
        }


manager = CalculatorManager()
