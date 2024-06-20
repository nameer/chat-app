from datetime import UTC, datetime
from typing import Annotated
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field, field_validator

from app.core.config import settings

from .base import PhoneNumberStr


class OTPRequest(BaseModel):
    phone_number: PhoneNumberStr


class OTPVerify(BaseModel):
    phone_number: PhoneNumberStr
    OTP: Annotated[
        str,
        Field(
            min_length=settings.OTP_LENGTH,
            max_length=settings.OTP_LENGTH,
            pattern=rf"\d{{{settings.OTP_LENGTH}}}",
        ),
    ]


class TokenPayload(BaseModel):
    token_id: UUID4 = Field(default_factory=uuid4)

    user_id: int
    user_credential_id: int | None = None

    issued_at: datetime | None = None

    @field_validator("issued_at")
    @classmethod
    def convert_to_utc_offset_naive(cls, v: datetime | None) -> datetime | None:
        if v is not None:
            v = v.astimezone(UTC).replace(tzinfo=None)
        return v


class Token(BaseModel):
    access_token: str

    token_type: str
    expires_in: int