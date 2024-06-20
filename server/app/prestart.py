#!/usr/local/bin/python

import alembic.config
from sqlalchemy import text
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.logger import logger
from app.db.session import SessionLocal

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1

retrier = retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, "INFO"),
    after=after_log(logger, "WARNING"),
)


@retrier
def init_db_service() -> None:
    try:
        with SessionLocal() as db:
            # Try to create session to check if DB is awake
            db.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(e)
        raise


def db_migration() -> None:
    args = ["upgrade", "head"]
    alembic.config.main(argv=args)


def main() -> None:
    logger.info("Initializing database service")
    init_db_service()
    logger.info("Database service finished initializing")

    logger.info("Starting database migration")
    db_migration()
    logger.info("Database migration finished")


if __name__ == "__main__":
    main()
