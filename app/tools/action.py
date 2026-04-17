import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any

from app.core.logging import get_logger

ACTIONS: dict[str, dict[str, Callable[..., Any]]] = {}


def action(
    action_id: str | None = None,
    *,
    group: str = "default",
    enable_logging: bool = False,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        resolved_action_id: str = action_id or func.__name__
        logger = get_logger(group)

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if enable_logging:
                logger.info("Action '%s' started", resolved_action_id)

            try:
                result: Any = func(*args, **kwargs)
                logger.debug(
                    "Action '%s' input:\n%s\n%s\nAction '%s' out:\n'%s'",
                    resolved_action_id,
                    [*args],
                    {**kwargs},
                    resolved_action_id,
                    result,
                )
            except Exception:
                if enable_logging:
                    logger.exception("Action '%s' failed", resolved_action_id)
                raise

            if enable_logging:
                logger.info("Action '%s' completed", resolved_action_id)

            return result

        wrapper.__action_group__ = group
        wrapper.__action_id__ = resolved_action_id
        return wrapper

    return decorator


def register_action_handler(handler: Callable[..., Any]) -> None:
    group: str | None = getattr(handler, "__action_group__", None)
    action_id: str | None = getattr(handler, "__action_id__", None)

    if not group or not action_id:
        return

    ACTIONS.setdefault(group, {})[action_id] = handler


def register_action_handlers(instance: object) -> None:
    for attribute_name in dir(instance):
        attribute = getattr(instance, attribute_name)
        if callable(attribute):
            register_action_handler(attribute)


def get_action_handler(group: str, action_id: str) -> Callable[..., Any]:
    try:
        return ACTIONS[group][action_id]
    except KeyError as exc:
        raise KeyError(f"Action '{action_id}' not found in group '{group}'") from exc


def run_action_handler(handler: Callable[..., Any], action_input: dict[str, Any]) -> Any:
    signature = inspect.signature(handler)
    parameters = list(signature.parameters.values())

    if not parameters:
        return handler()

    has_var_keyword: bool = any(parameter.kind is inspect.Parameter.VAR_KEYWORD for parameter in parameters)
    if has_var_keyword:
        return handler(**action_input)

    if len(parameters) == 1 and parameters[0].name == "input_data":
        return handler(action_input)

    kwargs: dict[str, Any] = {}
    missing_required: list[str] = []

    for parameter in parameters:
        if parameter.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ):
            continue

        if parameter.name in action_input:
            kwargs[parameter.name] = action_input[parameter.name]
            continue

        if parameter.default is inspect._empty:
            missing_required.append(parameter.name)

    if missing_required:
        raise ValueError(f"Missing action input fields: {missing_required}")

    return handler(**kwargs)
