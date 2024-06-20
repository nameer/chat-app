import sys

from app.core.config import settings
from loguru import logger

level = settings.LOGGING.LEVEL
serialize = settings.LOGGING.SERIALIZE

logger.remove()

if level in {"ERROR", "CRITICAL"}:
    logger.add(
        sys.stderr,
        serialize=serialize,
        backtrace=True,
        diagnose=True,
        level=level,
    )
else:
    logger.add(
        sys.stdout,
        serialize=serialize,
        backtrace=True,
        diagnose=True,
        level=level,
    )
    logger.add(
        sys.stderr,
        serialize=serialize,
        backtrace=True,
        diagnose=True,
        level="ERROR",
    )
