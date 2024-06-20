from typing import Any

from sqlalchemy.orm import as_declarative, declared_attr
from sqlalchemy.sql.schema import MetaData


@as_declarative()
class Base:
    __name__: str

    id: Any
    metadata: MetaData

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    # Generate __tablename__ automatically
    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__
