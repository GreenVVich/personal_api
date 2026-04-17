import logging
from datetime import datetime
from pathlib import Path

from app.core.config import settings

LOG_FORMAT: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
LOGS_DIR: Path = Path(__file__).resolve().parent.parent / "logs"
LOG_LEVEL: int = getattr(logging, settings.LOG_LEVEL, logging.INFO)
LOG_FILE: Path = LOGS_DIR / f"app_{datetime.now().strftime('%d-%m-%Y')}.log"

LOGS_DIR.mkdir(parents=True, exist_ok=True)

_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
_handler.setFormatter(logging.Formatter(LOG_FORMAT))
_loggers: dict[str, logging.Logger] = {}


def get_logger(name: str = "api") -> logging.Logger:
    if name in _loggers:
        return _loggers[name]

    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False

    if _handler not in logger.handlers:
        logger.addHandler(_handler)

    _loggers[name] = logger
    return logger
