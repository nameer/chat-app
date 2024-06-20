from datetime import timedelta
from typing import Annotated

from app import crud
from app import schemas as s
from app.core.config import settings
from app.core.security.token import AccessToken
from app.deps import get_db_session
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/request-otp",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=s.auth.OTPInfo,
    responses={
        429: {
            "description": "Too many requests",
            "content": {
                "application/json": {
                    "example": {"detail": "You have reached limit for OTP requests"}
                }
            },
        }
    },
)
def request_otp(data: s.auth.OTPRequest) -> dict:
    # TODO:
    #   1. Generate OTP
    #   2. Get attempts from redis. If already exeeded, raise 429
    #   2. Save phonenumber-OTP map in Redis, with ttl, and update attempts
    #   3. Send OTP to mobile
    return {"expires_in": 500}


@router.post(
    "/verify-otp",
    response_model=s.auth.Token,
    responses={
        401: {
            "description": "Wrong or expired OTP",
            "content": {
                "application/json": {"example": {"detail": "Wrong or expired OTP"}}
            },
        }
    },
)
def validate_otp(
    session: Annotated[Session, Depends(get_db_session)],
    data: s.auth.OTPVerify,
) -> dict:
    # TODO:
    #   1. Get OTP from Redis using phone-number. Raise 401 if not found
    #   2. Check if OTPs match
    #   3. a. If matches,
    #         i.  remove OTP from redis
    #         ii. generate and send token(s)
    #      b. If doesn't match, raise 401, raise attempt count

    user = crud.user.get_by_phone_number(session, data.phone_number)
    if not user:
        crud.user.create(session, s.user.UserCreate(phone_number=data.phone_number))

    payload = s.auth.TokenPayload(user_id=user.id)
    access_token_exp = timedelta(minutes=settings.ACCESS_TOKEN.EXPIRE_MINUTES)
    access_token = AccessToken.create(payload, expires_delta=access_token_exp)

    return {
        "access_token": access_token,
        "expires_in": access_token_exp.total_seconds(),
    }
