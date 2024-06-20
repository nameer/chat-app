from datetime import datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator

from .user import User


# Shared properties
class ChatBase(BaseModel):
    is_group: bool


# -- Create schema -- #


# Properties to receive via API on creation
class ChatCreate(ChatBase):
    members: list[int]  # Only others

    @model_validator(mode="after")
    def valid_member_count(self) -> Self:
        if not self.is_group:
            assert (
                len(self.members) == 1
            ), "A private chat cannot have more than one member"
        return self


# Properties to be stored in the DB on creation
class ChatInDBCreate(ChatBase):
    pass


# -- Update schema -- #


# Properties to be stored in the DB on update
class UserInDBUpdate(BaseModel):
    pass


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
    results: list[Chat]
    total_count: int
