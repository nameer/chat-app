from typing import Annotated

from app import crud
from app import models as m
from app import schemas as s
from app.deps import get_chat, get_db_session, get_user
from app.endpoints.helper import notify_members
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("", response_model=s.message.Message)
def add_message(
    session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[m.User, Depends(get_user)],
    chat: Annotated[m.Chat, Depends(get_chat)],
    background_tasks: BackgroundTasks,
    data: s.message.MessageCreate,
) -> s.message.Message:
    msg_out = crud.message.create(
        session,
        s.message.MessageInDBCreate(
            **data.model_dump(),
            sender_id=current_user.id,
            chat_id=chat.id,
        ),
    )
    message = s.message.Message.model_validate(msg_out)
    background_tasks.add_task(notify_members, message)
    return message


@router.get("", response_model=s.message.MessageList)
def list_messages(
    session: Annotated[Session, Depends(get_db_session)],
    pagination: Annotated[s.search.Pagination, Depends()],
) -> dict:
    results, total_count = crud.message.get_multi(
        session,
        token=(m.Message.created_at, pagination.token),
        limit=pagination.limit,
        order_by=m.Message.created_at.desc(),
    )
    return {"results": results, "total_count": total_count}
