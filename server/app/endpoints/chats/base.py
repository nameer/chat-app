from typing import Annotated

from app import crud
from app import models as m
from app import schemas as s
from app.deps import get_db_session, get_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("", response_model=s.chat.ChatWithMembers)
def create_chat(
    session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[m.User, Depends(get_user)],
    data: s.chat.ChatCreate,
) -> m.Chat:
    member_ids = {current_user.id, *data.members}
    if len(member_ids) == 1:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="No member to start chat with"
        )

    if not data.is_group:
        chat = crud.chat.get_private_chat(session, member_ids=member_ids)
        if chat:
            # A private chat already exists
            return chat
    else:
        raise HTTPException(
            status.HTTP_501_NOT_IMPLEMENTED,
            detail="Group creation is not supported yet",
        )

    if not crud.user.exists(session, ids=data.members):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="One or more users were not found"
        )

    chat = crud.chat.new(session, data, creator=current_user)
    return chat


@router.get("", response_model=s.chat.ChatList)
def search_chats(
    session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[m.User, Depends(get_user)],
    search: Annotated[s.search.Search, Depends()],
) -> dict:
    results, total_count = crud.chat.search(session, user=current_user, search=search)
    return {"results": results, "total_count": total_count}
