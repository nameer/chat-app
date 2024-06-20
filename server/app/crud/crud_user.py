from typing import Iterable

from pydantic import TypeAdapter
from sqlalchemy import ColumnElement
from sqlalchemy.orm import Session

from app import models as m
from app import schemas as s
from app.schemas.base import PhoneNumberStr

from .base import CRUDBase


class CRUDUser(CRUDBase[m.User, s.user.UserInDBCreate, s.user.UserInDBUpdate]):
    def exists(self, session: Session, /, ids: Iterable[int]) -> bool:
        return self.get_count(session, filters=[m.User.id.in_(ids)]) == len(ids)

    def get_by_phone_number(self, session: Session, /, phone_number: str) -> m.User:
        return self.get(session, filters=[m.User.phone_number == phone_number])

    def search(
        self, session: Session, /, current_user: m.User, search: s.search.Search
    ) -> tuple[list[m.User], int]:
        term_filter: ColumnElement
        try:
            TypeAdapter.validate_python(TypeAdapter(PhoneNumberStr), search.term)
            term_filter = m.User.phone_number == search.term
        except Exception:
            term_filter = m.User.name.ilike(f"%{search.term}%")

        return self.get_multi(
            session,
            token=(m.User.created_at, search.token),
            limit=search.limit,
            filters=[term_filter, m.User.id != current_user.id],
            order_by=m.User.created_at,
        )


user = CRUDUser(m.User)
