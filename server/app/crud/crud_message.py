from app import models as m
from app import schemas as s

from .base import CRUDBase


class CRUDMessage(
    CRUDBase[m.Message, s.message.MessageInDBCreate, s.message.MessageInDBUpdate]
):
    pass


message = CRUDMessage(m.Message)
