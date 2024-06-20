from datetime import UTC, datetime

from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

from .chat import Chat


class Message(Base):
    id: Mapped[int] = mapped_column(primary_key=True)

    chat_id: Mapped[int] = mapped_column(ForeignKey("Chat.id"))
    sender_id: Mapped[int] = mapped_column(ForeignKey("User.id"))

    content: Mapped[str | None]
    is_edited: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    last_updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    chat: Mapped[Chat] = relationship(back_populates="messages")

    @hybrid_property
    def is_deleted(self) -> bool:
        return self.content.is_(None)
