from datetime import UTC, datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

from .chat import Chat


class Message(Base):
    id: Mapped[int] = mapped_column(primary_key=True)

    chat_id: Mapped[int] = mapped_column(ForeignKey("Chat.id"))
    sender_id: Mapped[int] = mapped_column(ForeignKey("User.id"))

    content: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    chat: Mapped[Chat] = relationship()
