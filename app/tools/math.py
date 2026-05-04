from typing import Any

from app.box.runtime import action


def _as_number(value: Any, *, name: str) -> float:
    if not isinstance(value, int | float):
        raise ValueError(f"{name} must be numeric")
    return float(value)


def _as_numeric_args(values: list[Any], *, function_name: str) -> list[float]:
    return [_as_number(value, name=f"{function_name}[{index}]") for index, value in enumerate(values)]


def _as_numeric_kwargs(values: dict[str, Any]) -> dict[str, float]:
    return {key: _as_number(value, name=key) for key, value in values.items()}


@action("assign")
def assign(value: Any) -> float:
    return _as_number(value, name="value")


@action("sum")
def sum_values(*args: Any, **kwargs: Any) -> float:
    if args and kwargs:
        raise ValueError("sum accepts either positional or keyword arguments")
    if args:
        return float(sum(_as_numeric_args(list(args), function_name="sum")))
    return float(sum(_as_numeric_kwargs(kwargs).values()))


@action("multiply")
def multiply(*args: Any, **kwargs: Any) -> float:
    if args and kwargs:
        raise ValueError("multiply accepts either positional or keyword arguments")

    values = (
        _as_numeric_args(list(args), function_name="multiply") if args else list(_as_numeric_kwargs(kwargs).values())
    )
    result = 1.0
    for value in values:
        result *= value
    return result


@action("divide")
def divide(dividend: Any, divisor: Any) -> float:
    left = _as_number(dividend, name="dividend")
    right = _as_number(divisor, name="divisor")
    if right == 0:
        raise ValueError("divisor must not be zero")
    return left / right


@action("subtract")
def subtract(minuend: Any, subtrahend: Any) -> float:
    return _as_number(minuend, name="minuend") - _as_number(subtrahend, name="subtrahend")


@action("power")
def power(base: Any, exponent: Any) -> float:
    return _as_number(base, name="base") ** _as_number(exponent, name="exponent")


@action("sqrt")
def sqrt(value: Any) -> float:
    number = _as_number(value, name="value")
    if number < 0:
        raise ValueError("value must be greater than or equal to zero")
    return number**0.5


@action("round")
def round_value(value: Any, digits: Any = 0) -> float:
    return float(round(_as_number(value, name="value"), int(_as_number(digits, name="digits"))))
