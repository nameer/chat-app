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

    is_group: Mapped[bool] = mapped_column()

    created_by: Mapped[datetime] = mapped_column(ForeignKey("User.id"))
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    members: Mapped[list[User]] = relationship(
        secondary="ChatMember",
        back_populates="chats",
    )
    messages: Mapped[list["Message"]] = relationship(
        lazy="dynamic",
        back_populates="chat",
    )


class ChatMember(Base):
    chat_id: Mapped[int] = mapped_column(ForeignKey("Chat.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"), primary_key=True)

    joined_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
