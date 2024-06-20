from sqlalchemy.orm import Session

from app import models as m
from app import schemas as s

from .base import CRUDBase


class CRUDUser(CRUDBase[m.User, s.user.UserInDBCreate, s.user.UserInDBUpdate]):
    def get_by_phone_number(self, session: Session, phone_number: str) -> m.User:
        return self.get(session, filters=[m.User.phone_number == phone_number])


user = CRUDUser(m.User)
