from contextlib import contextmanager

from app import crud
from app import schemas as s
from app.core.notification import notification_manager
from app.deps import get_db_session
from fastapi.concurrency import contextmanager_in_threadpool


async def notify_members(message: s.message.Message) -> None:
    async with contextmanager_in_threadpool(
        contextmanager(get_db_session)()
    ) as session:
        member_objs = crud.chat.get(session, id=message.chat_id).members
        member_ids = [member.id for member in member_objs]

    for member_id in member_ids:
        await notification_manager.broadcast(member_id, message)
