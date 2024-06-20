from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
)


# Shared properties
class MessageBase(BaseModel):
    chat_id: int

    content: str | None


# -- Create schema -- #


# Properties to receive via API on creation
class MessageCreate(MessageBase):
    content: str


# Properties to be stored in the DB on creation
class MessageInDBCreate(MessageCreate):
    sender_id: int


# -- Update schema -- #


# Properties to be stored in the DB on update
class MessageInDBUpdate(BaseModel()):
    pass


# -- Read schema -- #


# Additional properties to return via API
class Message(MessageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sender_id: int

    is_edited: bool
    is_deleted: bool

    created_at: datetime
    last_updated_at: datetime


# --- --- --- #


class MessageList(BaseModel):
    results: list[Message]
    total_count: int