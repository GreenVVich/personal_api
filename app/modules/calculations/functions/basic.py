from typing import Any

from app.tools.registry import register


def _as_number(value: Any, *, name: str) -> float:
    if not isinstance(value, int | float):
        raise ValueError(f"{name} must be numeric")
    return float(value)


def _as_numeric_kwargs(values: dict[str, Any]) -> dict[str, float]:
    return {key: _as_number(value, name=key) for key, value in values.items()}


def _as_numeric_args(values: list[Any], *, function_name: str) -> list[float]:
    return [
        _as_number(value, name=f"{function_name}[{index}]") for index, value in enumerate(values)
    ]


@register("value")
def value(value: Any) -> float:
    return _as_number(value, name="value")


@register("sum")
def sum_values(*args: Any, **kwargs: Any) -> float:
    if args and kwargs:
        raise ValueError("sum accepts either positional or keyword arguments")
    if args:
        return float(sum(_as_numeric_args(list(args), function_name="sum")))
    return float(sum(_as_numeric_kwargs(kwargs).values()))


@register("multiply")
def multiply(*args: Any, **kwargs: Any) -> float:
    if args and kwargs:
        raise ValueError("multiply accepts either positional or keyword arguments")

    values: list[float]
    if args:
        values = _as_numeric_args(list(args), function_name="multiply")
    else:
        values = list(_as_numeric_kwargs(kwargs).values())

    result: float = 1.0
    for value in values:
        result *= value
    return result


@register("divide")
def divide(dividend: Any, divisor: Any) -> float:
    left: float = _as_number(dividend, name="dividend")
    right: float = _as_number(divisor, name="divisor")
    if right == 0:
        raise ValueError("divisor must not be zero")
    return left / right


@register("subtract")
def subtract(minuend: Any, subtrahend: Any) -> float:
    left: float = _as_number(minuend, name="minuend")
    right: float = _as_number(subtrahend, name="subtrahend")
    return left - right


@register("power")
def power(base: Any, exponent: Any) -> float:
    left: float = _as_number(base, name="base")
    right: float = _as_number(exponent, name="exponent")
    return left**right


@register("sqrt")
def sqrt(value: Any) -> float:
    number: float = _as_number(value, name="value")
    if number < 0:
        raise ValueError("value must be greater than or equal to zero")
    return number**0.5


@register("round")
def round_value(value: Any, digits: Any = 0) -> float:
    number: float = _as_number(value, name="value")
    precision: float = _as_number(digits, name="digits")
    return float(round(number, int(precision)))
