from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

from .user import User

if TYPE_CHECKING:
    from .message import Message


class Chat(Base):
    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    last_updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    users: Mapped[list[User]] = relationship(secondary="ChatMember")
    messages: Mapped[list["Message"]] = relationship(lazy="dynamic")


class ChatMember(Base):
    chat_id: Mapped[int] = mapped_column(ForeignKey("Chat.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"), primary_key=True)

    joined_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
