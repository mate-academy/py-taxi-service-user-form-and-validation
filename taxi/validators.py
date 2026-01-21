from typing import AnyStr

from django.core.exceptions import ValidationError


def license_number_validator(license_number: str) -> AnyStr:
    if len(license_number) != 8:
        raise ValidationError(
            "License number must be 8 characters long."
        )

    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError(
            "License number must start with 3 uppercase letter."
        )

    if not license_number[3:].isdigit():
        raise ValidationError(
            "License number must end with 5 digits."
        )
    return license_number
