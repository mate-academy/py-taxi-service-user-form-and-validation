import re

from django.core.exceptions import ValidationError


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError(
            "License number must be exactly 8 characters long."
        )

    if not re.match(r"^[A-Z]{3}[0-9]{5}$", license_number):
        raise ValidationError(
            "The last 5 characters must be digits."
        )

    return license_number
