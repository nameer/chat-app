from datetime import datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator

from .user import User


# Shared properties
class ChatBase(BaseModel):
    name: str | None
    is_group: bool

    @model_validator(mode="after")
    def fields_present(self) -> Self:
        assert bool(self.name) is bool(
            self.is_group
        ), "Naming is supported only for groups"
        return self


# -- Create schema -- #


# Properties to receive via API on creation
class ChatCreate(ChatBase):
    members: set[int]  # Only others

    @model_validator(mode="after")
    def valid_member_count(self) -> Self:
        if not self.is_group:
            assert (
                len(self.members) == 1
            ), "A private chat cannot have more than one member"
        return self


# Properties to be stored in the DB on creation
class ChatInDBCreate(ChatBase):
    created_by: int


# -- Update schema -- #


# Properties to be stored in the DB on update
class ChatInDBUpdate(BaseModel):
    name: str


# -- Read schema -- #


# Additional properties to return via API
class Chat(ChatBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class ChatWithMembers(Chat):
    members: list[User]


# --- --- --- #


class ChatList(BaseModel):
    results: list[ChatWithMembers]
    total_count: int
