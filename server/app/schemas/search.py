from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt

from .base import PhoneNumberStr


class Pagination(BaseModel):
    token: datetime | None = None
    limit: PositiveInt


class Search(Pagination):
    term: PhoneNumberStr | Annotated[str, Field(min_length=3)] | None = None
