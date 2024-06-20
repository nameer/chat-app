from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    str(settings.DATABASE.URI),
    pool_pre_ping=True,
    echo=settings.DATABASE.ECHO_QUERY,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
