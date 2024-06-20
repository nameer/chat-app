from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, Relationship, mapped_column, relationship

from app.db.base_class import Base

from .user import User

if TYPE_CHECKING:
    from .message import Message


class Chat(Base):
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str | None] = mapped_column(String(20))
    is_group: Mapped[bool] = mapped_column()

    created_by: Mapped[datetime] = mapped_column(ForeignKey("User.id"))
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    members: Mapped[list[User]] = relationship(
        secondary="ChatMember",
        back_populates="chats",
        viewonly=True,
    )
    messages: Relationship[list["Message"]] = relationship(
        lazy="dynamic",
        back_populates="chat",
    )

    memberships: Relationship[list["ChatMember"]] = relationship(
        lazy="dynamic",
        back_populates="chat",
    )


class ChatMember(Base):
    chat_id: Mapped[int] = mapped_column(ForeignKey("Chat.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"), primary_key=True)

    joined_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    chat: Mapped[Chat] = relationship(back_populates="memberships")
    member: Mapped[User] = relationship(back_populates="memberships")
