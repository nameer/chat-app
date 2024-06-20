import sys

from loguru import logger

from app.core.config import settings

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
