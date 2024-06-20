from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
)

from .base import NonEmptyStr, PhoneNumberStr


# Shared properties
class UserBase(BaseModel):
    name: NonEmptyStr | None = None
    phone_number: PhoneNumberStr


# -- Create schema -- #


# Properties to receive via API on creation
class UserCreate(UserBase):
    pass


# Properties to be stored in the DB on creation
class UserInDBCreate(UserBase):
    pass


# -- Update schema -- #


# Properties to receive via API on update
class UserUpdate(BaseModel):
    name: NonEmptyStr


# Properties to be stored in the DB on update
class UserInDBUpdate(UserUpdate):
    pass


# -- Read schema -- #


# Additional properties to return via API
class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

    created_at: datetime
    last_updated_at: datetime


# --- --- --- #


class UserList(BaseModel):
    results: list[User]
    total_count: int
