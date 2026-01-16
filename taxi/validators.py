from django.core.exceptions import ValidationError
import re


def validate_license_number(value: str) -> None:
    if (len(value) != 8
            or not re.match(r"^[A-Z]{3}\d{5}$", value)):
        raise ValidationError(
            "There must be exactly 8 characters: "
            "the first 3 are uppercase letters, "
            "the last 5 are numbers."
        )
