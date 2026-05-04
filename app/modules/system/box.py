from app.box.core import Box, BoxAction

system_box = Box(
    name="system",
    cells={
        "current_datetime": None,
        "system_stats": {},
        "docker_containers": [],
        "last_snapshot": {},
    },
    actions={
        "refresh_snapshot": BoxAction(
            handler="system.refresh_snapshot",
            description="Refresh current datetime, system stats and docker containers",
        ),
        "get_snapshot": BoxAction(
            handler="system.get_snapshot",
            description="Get the latest cached snapshot from the system box",
        ),
        "list_docker_containers": BoxAction(
            handler="system.list_docker_containers",
            description="Fetch currently running docker containers",
        ),
        "run_cmd": BoxAction(
            handler="system.run_cmd",
            args={"command": {"$input": "command"}},
            description="Run shell command and return stdout/stderr/exit_code",
        ),
    },
)
