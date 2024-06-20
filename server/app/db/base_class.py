from typing import Any

from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.sql.schema import MetaData


class Base(DeclarativeBase):
    __name__: str

    id: Any
    metadata: MetaData

    # Generate __tablename__ automatically
    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__
