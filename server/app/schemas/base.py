from typing import Annotated

from pydantic import SecretStr, StringConstraints
from pydantic.functional_validators import AfterValidator
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.core.config import settings

__all__ = (
    "CleanStr",
    "NonEmptyStr",
    "OptionalNonEmptyStr",
    "PasswordStr",
    "PhoneNumberStr",
    "validate_not_none",
)


class PhoneNumberStr(PhoneNumber):
    # We are overriding the class variable here. An open issue for more optimal
    # usage is here: https://github.com/pydantic/pydantic-extra-types/issues/107
    default_region_code = settings.DEFAULT_REGION_CODE
    phone_format = "E164"


def validate_not_none(value: str | None) -> str:
    assert value is not None, "none is not an allowed value"
    return value


CleanStr = Annotated[str, StringConstraints(strip_whitespace=True)]
NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
OptionalNonEmptyStr = Annotated[NonEmptyStr | None, AfterValidator(validate_not_none)]
PasswordStr = Annotated[SecretStr, StringConstraints(min_length=8)]
