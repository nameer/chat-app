from pydantic import TypeAdapter
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, aliased, joinedload

from app import models as m
from app import schemas as s
from app.schemas.base import PhoneNumberStr

from .base import CRUDBase, SaveAction


class CRUDChat(CRUDBase[m.Chat, s.chat.ChatInDBCreate, s.chat.ChatInDBUpdate]):
    def new(
        self,
        session: Session,
        /,
        data: s.chat.ChatCreate,
        creator: m.User,
        *,
        action: SaveAction = SaveAction.COMMIT,
    ) -> m.Chat:
        chat = self.create(
            session,
            s.chat.ChatInDBCreate(
                name=data.name, is_group=data.is_group, created_by=creator.id
            ),
            action=SaveAction.FLUSH,
        )
        memberships = [
            m.ChatMember(chat_id=chat.id, user_id=uid)
            for uid in {creator.id, *data.members}
        ]
        chat.memberships = memberships
        self.handle_session(session, action=action)
        return chat

    def get_private_chat(
        self, session: Session, /, member_ids: tuple[int, int]
    ) -> m.Chat | None:
        mem1, mem2 = member_ids
        ChatMember1 = aliased(m.ChatMember)
        ChatMember2 = aliased(m.ChatMember)

        return session.scalars(
            select(m.Chat).where(
                m.Chat.id.in_(
                    select(ChatMember1.chat_id)
                    .join(ChatMember2, ChatMember1.chat_id == ChatMember2.chat_id)
                    .where(ChatMember1.user_id == mem1, ChatMember2.user_id == mem2)
                ),
                m.Chat.is_group.is_(False),
            )
        ).one_or_none()

    def search(
        self, session: Session, /, user: m.User, search: s.search.Search
    ) -> tuple[list[m.Chat], int]:
        if search.term:
            try:
                TypeAdapter.validate_python(TypeAdapter(PhoneNumberStr), search.term)
                term_filter = m.User.phone_number == search.term
            except Exception:
                term_filter = or_(
                    m.Chat.name.ilike(f"%{search.term}%"),
                    m.User.name.ilike(f"%{search.term}%"),
                )
        else:
            term_filter = None

        stmt = (
            select(m.Chat)
            .where(
                m.Chat.id.in_(
                    select(m.Chat.id)
                    .join(m.ChatMember, m.Chat.id == m.ChatMember.chat_id)
                    .where(m.ChatMember.user_id == user.id)
                )
            )
            .join(m.ChatMember, m.Chat.id == m.ChatMember.chat_id)
            .join(m.User, m.ChatMember.user_id == m.User.id)
        )
        if term_filter is not None:
            stmt = stmt.where(term_filter, m.User.id != user.id)
        stmt = stmt.options(joinedload(m.Chat.members))
        total_count = session.scalar(stmt.with_only_columns(func.count()))

        if search.token:
            stmt = stmt.where(m.Chat.created_at > search.token)
        stmt = stmt.limit(search.limit).order_by(m.Chat.created_at)

        return session.scalars(stmt).unique(), total_count


chat = CRUDChat(m.Chat)
