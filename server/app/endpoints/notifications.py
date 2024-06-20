from contextlib import contextmanager
from typing import Annotated

from app import crud
from app import models as m
from app import schemas as s
from app.core.notification import notification_manager
from app.deps import get_db_session, get_user
from app.endpoints.helper import notify_members
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.concurrency import contextmanager_in_threadpool
from pydantic import ValidationError

router = APIRouter()


async def add_message(
    user: m.User,
    message: s.message.MessageWSCreate,
) -> s.message.Message:
    async with contextmanager_in_threadpool(
        contextmanager(get_db_session)()
    ) as session:
        if not crud.user.has_chat(session, user, message.chat_id):
            return
        msg_out = crud.message.create(
            session,
            s.message.MessageInDBCreate(**message.model_dump(), sender_id=user.id),
        )
        return s.message.Message.model_validate(msg_out)


@router.websocket("/search")
async def message_notifier(
    websocket: WebSocket, current_user: Annotated[m.User, Depends(get_user)]
):
    await notification_manager.connect(current_user.id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            try:
                msg_in = s.message.MessageWSCreate(**data)
            except ValidationError:
                # Not properly formatted or invalid. Discard
                continue
            message = add_message(current_user, message=msg_in)
            notify_members(message)
    except WebSocketDisconnect:
        await notification_manager.disconnect(current_user.id, websocket)
