from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, Relationship, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .chat import Chat, ChatMember


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str | None] = mapped_column(String(30))

    phone_number: Mapped[str] = mapped_column(String(15), unique=True)

    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    last_updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    chats: Mapped[list["Chat"]] = relationship(
        secondary="ChatMember", back_populates="members", viewonly=True
    )

    memberships: Relationship[list["ChatMember"]] = relationship(
        lazy="dynamic",
        back_populates="member",
    )
