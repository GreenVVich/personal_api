from __future__ import annotations

import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any

from app.box.core import Box, BoxAction
from app.core.logging import get_logger

ACTION_HANDLERS: dict[str, Callable[..., Any]] = {}


def action(name: str, *, enable_logging: bool = False) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        logger = get_logger(f"action.{name}")

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if enable_logging:
                logger.info("Action '%s' started", name)

            try:
                result = func(*args, **kwargs)
            except Exception:
                if enable_logging:
                    logger.exception("Action '%s' failed", name)
                raise

            if enable_logging:
                logger.info("Action '%s' completed", name)
            logger.debug("Action '%s' args=%s kwargs=%s result=%s", name, args, kwargs, result)
            return result

        ACTION_HANDLERS[name] = wrapper
        wrapper.__action_name__ = name
        return wrapper

    return decorator


def get_action_handler(name: str) -> Callable[..., Any]:
    try:
        return ACTION_HANDLERS[name]
    except KeyError as exc:
        raise KeyError(f"Registered action '{name}' not found") from exc


def execute_action(
    box: Box,
    action_name: str,
    *,
    input_data: dict[str, Any] | None = None,
    repository: Any = None,
) -> Any:
    try:
        box_action: BoxAction = box.actions[action_name]
    except KeyError as exc:
        raise KeyError(f"Action '{action_name}' not found in box '{box.name}'") from exc

    handler = get_action_handler(box_action.handler)
    resolved_args = _resolve_value(box_action.args, box=box, input_data=input_data or {})
    return _invoke_handler(
        handler,
        box=box,
        action_name=action_name,
        input_data=input_data or {},
        repository=repository,
        resolved_args=resolved_args,
    )


def _resolve_value(value: Any, *, box: Box, input_data: dict[str, Any]) -> Any:
    name_index = box.get_name_index()

    if isinstance(value, dict):
        if set(value) == {"$cell"}:
            cell_name = str(value["$cell"])
            if cell_name not in name_index:
                raise KeyError(f"Cell '{cell_name}' not found in box '{box.name}'")
            return name_index[cell_name]
        if set(value) == {"$input"}:
            input_name = str(value["$input"])
            if input_name not in input_data:
                raise KeyError(f"Input '{input_name}' not found for box '{box.name}'")
            return input_data[input_name]
        if set(value) == {"$value"}:
            return value["$value"]
        return {key: _resolve_value(item, box=box, input_data=input_data) for key, item in value.items()}

    if isinstance(value, list):
        return [_resolve_value(item, box=box, input_data=input_data) for item in value]

    return value


def _invoke_handler(
    handler: Callable[..., Any],
    *,
    box: Box,
    action_name: str,
    input_data: dict[str, Any],
    repository: Any,
    resolved_args: Any,
) -> Any:
    signature = inspect.signature(handler)
    kwargs: dict[str, Any] = {}
    injectable = {
        "box": box,
        "action_name": action_name,
        "input_data": input_data,
        "repository": repository,
    }

    if isinstance(resolved_args, list):
        return handler(*resolved_args, **_collect_injected_kwargs(signature, injectable))

    if isinstance(resolved_args, dict):
        kwargs.update(resolved_args)
    elif resolved_args is not None:
        kwargs["value"] = resolved_args

    for parameter_name, parameter in signature.parameters.items():
        if parameter.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue
        if parameter_name in kwargs:
            continue
        if parameter_name in injectable:
            kwargs[parameter_name] = injectable[parameter_name]

    return handler(**kwargs)


def _collect_injected_kwargs(signature: inspect.Signature, injectable: dict[str, Any]) -> dict[str, Any]:
    kwargs: dict[str, Any] = {}
    for parameter_name, parameter in signature.parameters.items():
        if parameter.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue
        if parameter_name in injectable:
            kwargs[parameter_name] = injectable[parameter_name]
    return kwargs
