from loguru import logger

from backend.config import config

logger.remove()

logger.add(
    sink="backend/logging/logs/{time:DD-MM-YYYY}.log",
    rotation="00:00",
    format="{time:HH:mm:ss DD-MM-YYYY} | {level: <8} | {message}",
    backtrace=False,
    level="DEBUG" if config.DEBUG else "INFO",
)

log = logger
