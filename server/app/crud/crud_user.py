from sqlalchemy import ColumnElement
from sqlalchemy.orm import Session

from app import models as m
from app import schemas as s
from app.schemas.base import PhoneNumberStr

from .base import CRUDBase


class CRUDUser(CRUDBase[m.User, s.user.UserInDBCreate, s.user.UserInDBUpdate]):
    def get_by_phone_number(self, session: Session, /, phone_number: str) -> m.User:
        return self.get(session, filters=[m.User.phone_number == phone_number])

    def search(
        self, session: Session, /, search: s.search.Search
    ) -> tuple[list[m.User], int]:
        term_filter: ColumnElement
        try:
            PhoneNumberStr(search.term)
            term_filter = m.User.phone_number == search.term
        except Exception:
            term_filter = m.User.name.ilike(search.term)

        return self.get_multi(
            session,
            token=(m.User.created_at, search.token),
            limit=search.limit,
            filters=[term_filter],
            order_by=m.User.created_at,
        )


user = CRUDUser(m.User)
