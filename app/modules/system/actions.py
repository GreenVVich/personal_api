from __future__ import annotations

import json
import os
import platform
import subprocess
from datetime import UTC, datetime
from typing import Any

from app.box.core import Box
from app.box.runtime import action


def _run_command(command: str) -> dict[str, Any]:
    if not isinstance(command, str) or not command.strip():
        raise ValueError("command must be a non-empty string")

    process = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return {
        "command": command,
        "exit_code": process.returncode,
        "stdout": (process.stdout or "").strip(),
        "stderr": (process.stderr or "").strip(),
    }


def _read_system_stats() -> dict[str, Any]:
    memory_command = (
        "powershell -NoProfile -Command "
        '"Get-CimInstance Win32_OperatingSystem | '
        'Select-Object TotalVisibleMemorySize,FreePhysicalMemory,LastBootUpTime | ConvertTo-Json -Compress"'
    )
    cpu_command = (
        "powershell -NoProfile -Command "
        "\"Get-Counter '\\Processor(_Total)\\% Processor Time' | "
        "Select-Object -ExpandProperty CounterSamples | "
        'Select-Object -ExpandProperty CookedValue | ConvertTo-Json -Compress"'
    )

    memory_info: dict[str, Any] = {}
    cpu_load: float | None = None

    memory_result = _run_command(memory_command)
    if memory_result["exit_code"] == 0 and memory_result["stdout"]:
        try:
            raw_memory = json.loads(memory_result["stdout"])
            if isinstance(raw_memory, dict):
                total_kb = int(raw_memory["TotalVisibleMemorySize"])
                free_kb = int(raw_memory["FreePhysicalMemory"])
                last_boot_raw = str(raw_memory["LastBootUpTime"])
                last_boot_value: str = last_boot_raw
                if last_boot_raw.startswith("/Date(") and last_boot_raw.endswith(")/"):
                    try:
                        timestamp_ms = int(last_boot_raw.removeprefix("/Date(").removesuffix(")/"))
                        last_boot_value = datetime.fromtimestamp(timestamp_ms / 1000, tz=UTC).astimezone().isoformat()
                    except ValueError:
                        last_boot_value = last_boot_raw
                memory_info = {
                    "total_mb": round(total_kb / 1024, 2),
                    "free_mb": round(free_kb / 1024, 2),
                    "used_mb": round((total_kb - free_kb) / 1024, 2),
                    "last_boot_up_time": last_boot_value,
                }
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            memory_info = {"error": f"failed to parse memory stats: {exc}"}

    cpu_result = _run_command(cpu_command)
    if cpu_result["exit_code"] == 0 and cpu_result["stdout"]:
        try:
            raw_cpu_load = json.loads(cpu_result["stdout"])
            if raw_cpu_load is not None:
                cpu_load = round(float(raw_cpu_load), 2)
        except TypeError, ValueError, json.JSONDecodeError:
            cpu_load = None

    return {
        "platform": platform.platform(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
        "cpu_count": os.cpu_count(),
        "cpu_load_percent": cpu_load,
        "memory": memory_info,
    }


def _read_docker_containers() -> list[dict[str, Any]]:
    command = 'docker ps --format "{{json .}}"'
    result = _run_command(command)
    if result["exit_code"] != 0:
        return [{"error": result["stderr"] or "docker command failed"}]

    containers: list[dict[str, Any]] = []
    for line in result["stdout"].splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            containers.append(json.loads(line))
        except json.JSONDecodeError:
            containers.append({"raw": line})

    return containers


@action("system.run_cmd", enable_logging=True)
def run_cmd(command: str) -> dict[str, Any]:
    return _run_command(command)


@action("system.refresh_snapshot", enable_logging=True)
def refresh_snapshot(box: Box) -> dict[str, Any]:
    snapshot = {
        "current_datetime": datetime.now(UTC).astimezone().isoformat(),
        "stats": _read_system_stats(),
        "docker_containers": _read_docker_containers(),
    }
    box.cells["current_datetime"] = snapshot["current_datetime"]
    box.cells["system_stats"] = snapshot["stats"]
    box.cells["docker_containers"] = snapshot["docker_containers"]
    box.cells["last_snapshot"] = snapshot
    return snapshot


@action("system.get_snapshot")
def get_snapshot(box: Box) -> dict[str, Any]:
    return {
        "current_datetime": box.cells.get("current_datetime"),
        "system_stats": box.cells.get("system_stats"),
        "docker_containers": box.cells.get("docker_containers"),
    }


@action("system.list_docker_containers")
def list_docker_containers(box: Box) -> list[dict[str, Any]]:
    containers = _read_docker_containers()
    box.cells["docker_containers"] = containers
    return containers
