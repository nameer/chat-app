import datetime

from pydantic import BaseModel, PositiveInt

from .base import PhoneNumberStr


class Pagination(BaseModel):
    token: datetime
    limit: PositiveInt


class Search(Pagination):
    phone_number: PhoneNumberStr | None = None
    name: str | None = None
