from app.box.repository import box_repository
from app.modules.system import actions as _actions  # noqa: F401
from app.modules.system.box import system_box

box_repository.register(system_box)
