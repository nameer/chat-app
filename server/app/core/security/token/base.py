import abc
from dataclasses import KW_ONLY, dataclass
from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError

from app import schemas as s
from app.core.config import settings

ALGORITHM = "HS256"


def update_not_none(mapping: dict[Any, Any], **update: Any) -> None:
    mapping.update({k: v for k, v in update.items() if v is not None})


@dataclass
class JWTData:
    token_type: str

    sub: str  # Subject

    _: KW_ONLY
    include_iat: bool = True  # Include 'Issued At' or not
    jti: str | None = None  # JWT ID
    at_hash: str | None = None  # Access-token hash
    expires_delta: timedelta | None = None  # To calculate 'exp'


class JWTToken:
    @classmethod
    def create(cls, data: JWTData) -> str:
        to_encode: dict[str, Any] = {"sub": data.sub, "token_type": data.token_type}
        now = datetime.utcnow()
        if data.expires_delta:
            to_encode["exp"] = now + data.expires_delta
        if data.include_iat:
            to_encode["iat"] = now.timestamp()
        update_not_none(
            to_encode,
            jti=data.jti,
            at_hash=data.at_hash,
        )

        return jwt.encode(
            to_encode,
            settings.SECRET_KEY.get_secret_value(),
            algorithm=ALGORITHM,
        )

    @classmethod
    def decode(cls, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY.get_secret_value(),
                algorithms=[ALGORITHM],
            )
        except JWTError:
            msg = "Could not validate credentials"
            raise ValueError(msg) from None
        return payload


# --- --- --- #


class BaseToken(abc.ABC):
    TOKEN_TYPE: str

    @classmethod
    def create(
        cls,
        payload: s.auth.TokenPayload,
        *,
        expires_delta: timedelta | None = None,
    ) -> str:
        data = JWTData(
            cls.TOKEN_TYPE,
            str(payload.user_id),
            jti=str(payload.token_id),
            expires_delta=expires_delta,
        )
        return JWTToken.create(data)

    @classmethod
    def decode(cls, token: str) -> s.auth.TokenPayload:
        data = JWTToken.decode(token)
        if data.get("token_type") != cls.TOKEN_TYPE:
            msg = "Invalid token"
            raise ValueError(msg)

        try:
            payload = s.auth.TokenPayload(
                user_id=data["sub"],
                token_id=data.get("jti"),
                issued_at=data["iat"],
            )
        except (KeyError, ValidationError):
            msg = "Invalid token"
            raise ValueError(msg) from None

        return payload


# --- --- --- #


class AccessToken(BaseToken):
    TOKEN_TYPE: str = "access_token"
