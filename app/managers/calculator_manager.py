from app.data.calculators import load_calculators
from app.tools.registry import get
from app.modules.calculations.schemas import SCalculator


class CalculatorError(Exception):
    pass


class CalculatorManager:

    def load_raw(self):
        return load_calculators()

    def load(self):
        return self.load_raw()

    def get(self, calc_id: str) -> SCalculator:
        for c in self.load():
            if c.id == calc_id:
                return c
        raise CalculatorError(f"Calculator '{calc_id}' not found")

    def prepare_inputs(self, calc: SCalculator, data: dict):
        ctx = {}
        missing = []

        for i in calc.inputs:
            if i.id in data:
                ctx[i.id] = data[i.id]
            elif i.default is not None:
                ctx[i.id] = i.default
            elif i.required:
                missing.append(i.id)

        if missing:
            raise CalculatorError(f"Missing inputs: {missing}")

        return ctx

    def calculate(self, calc_id: str, data: dict):
        calc = self.get(calc_id)

        ctx = self.prepare_inputs(calc, data)

        # constants
        for k, v in calc.constants.items():
            ctx[k] = v.value

        results = {}
        text = []

        for v in calc.values:

            if v.function:
                func = get(v.function)

                # mapping param -> source
                args = {param: ctx.get(src) for param, src in v.args.items()}

                missing = [k for k, val in args.items() if val is None]
                if missing:
                    raise CalculatorError(f"{v.id}: missing {missing}")

                try:
                    value = func(**args)
                except Exception as e:
                    raise CalculatorError(f"{v.id}: {str(e)}")

            else:
                value = v.value

            if v.round is not None:
                value = round(value, v.round)

            ctx[v.id] = value
            results[v.id] = value

            if "Show" in v.tags and v.text_template:
                text.append(v.text_template.format(**ctx))

        return {
            "calculator": calc.id,
            "results": results,
            "text": "\n".join(text)
        }


manager = CalculatorManager()
