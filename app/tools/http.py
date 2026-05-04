from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from app.box.runtime import action


@action("http.request")
def http_request(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    query: dict[str, Any] | None = None,
    json_body: Any = None,
    body: str | bytes | None = None,
    timeout: float = 10,
) -> dict[str, Any]:
    request_url = _with_query(url, query)
    payload, request_headers = _build_payload(body=body, json_body=json_body, headers=headers or {})
    request = Request(request_url, data=payload, headers=request_headers, method=method.upper())

    try:
        with urlopen(request, timeout=timeout) as response:
            response_body = response.read()
            return _response_payload(
                url=request_url,
                status=response.status,
                headers=dict(response.headers.items()),
                body=response_body,
            )
    except HTTPError as exc:
        return _response_payload(
            url=request_url,
            status=exc.code,
            headers=dict(exc.headers.items()),
            body=exc.read(),
        )
    except URLError as exc:
        raise ConnectionError(f"HTTP request failed: {exc.reason}") from exc


@action("http.get")
def http_get(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    query: dict[str, Any] | None = None,
    timeout: float = 10,
) -> dict[str, Any]:
    return http_request(url, headers=headers, query=query, timeout=timeout)


def _with_query(url: str, query: dict[str, Any] | None) -> str:
    if not query:
        return url
    separator = "&" if "?" in url else "?"
    return f"{url}{separator}{urlencode(query, doseq=True)}"


def _build_payload(
    *,
    body: str | bytes | None,
    json_body: Any,
    headers: dict[str, str],
) -> tuple[bytes | None, dict[str, str]]:
    request_headers = dict(headers)
    if json_body is not None:
        request_headers.setdefault("Content-Type", "application/json")
        return json.dumps(json_body).encode("utf-8"), request_headers
    if isinstance(body, str):
        return body.encode("utf-8"), request_headers
    return body, request_headers


def _response_payload(url: str, status: int, headers: dict[str, str], body: bytes) -> dict[str, Any]:
    text = body.decode(_encoding_from_headers(headers), errors="replace")
    payload: dict[str, Any] = {
        "url": url,
        "status": status,
        "headers": headers,
        "text": text,
    }
    try:
        payload["json"] = json.loads(text)
    except json.JSONDecodeError:
        payload["json"] = None
    return payload


def _encoding_from_headers(headers: dict[str, str]) -> str:
    content_type = headers.get("Content-Type") or headers.get("content-type") or ""
    for part in content_type.split(";"):
        key, _, value = part.strip().partition("=")
        if key.lower() == "charset" and value:
            return value
    return "utf-8"
