from typing import Annotated, Generator

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app import crud
from app import models as m
from app import schemas as s
from app.core.security.token.base import AccessToken
from app.db.session import SessionLocal


def get_db_session() -> Generator:
    with SessionLocal() as session:
        yield session


def get_token(request: Request) -> str:
    signature = request.cookies.get("access_token_signature")
    header_payload = request.cookies.get("access_token_header_payload")
    if signature is None or header_payload is None:
        # If there is no signature, token is not present.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Cookie"},
        )
    return f"{header_payload}.{signature}"


def get_token_payload(token: Annotated[str, Depends(get_token)]) -> s.auth.TokenPayload:
    try:
        payload = AccessToken.decode(token)
    except ValueError as e:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Cookie"},
        ) from None
    return payload


def get_user(
    session: Annotated[Session, Depends(get_db_session)],
    payload: Annotated[s.auth.TokenPayload, Depends(get_token_payload)],
) -> m.User:
    if not (user := crud.user.get(session, id=payload.user_id)):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No such user")
    return user
