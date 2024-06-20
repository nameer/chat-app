from typing import Annotated

from app import crud
from app import models as m
from app import schemas as s
from app.deps import get_db_session, get_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("", response_model=s.user.UserList)
def search_users(
    session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[m.User, Depends(get_user)],
    search: Annotated[s.search.Search, Depends()],
) -> dict:
    results, total_count = crud.user.search(
        session,
        current_user=current_user,
        search=search,
    )
    return {"results": results, "total_count": total_count}


@router.get("/me", response_model=s.user.User)
def get_current_user_details(
    current_user: Annotated[m.User, Depends(get_user)]
) -> m.User:
    return current_user


@router.put("/me", response_model=s.user.User)
def update_current_user_details(
    session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[m.User, Depends(get_user)],
    data: s.user.UserUpdate,
) -> m.User:
    return crud.user.update(
        session,
        current_user,
        s.user.UserInDBUpdate(**data.model_dump(exclude_unset=True)),
    )


@router.get("/{user_id}", response_model=s.user.User)
def get_user_details(
    session: Annotated[Session, Depends(get_db_session)],
    user_id: int,
) -> m.User:
    if not (user := crud.user.get(session, id=user_id)):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No such user")
    return user
