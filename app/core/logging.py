import logging
from pathlib import Path

from app.core.config import settings


LOG_FORMAT: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
LOGS_DIR: Path = Path(__file__).resolve().parent.parent / "logs"
LOG_FILE: Path = LOGS_DIR / "app.log"

LOGS_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("api")
logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
logger.propagate = False

if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(file_handler)
