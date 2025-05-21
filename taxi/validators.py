from django.core.exceptions import ValidationError
import re


def validate_license_number(value):
    if not re.match(r"^[A-Z]{3}\d{5}$", value):
        raise ValidationError(
            "License number must be 3 uppercase letters followed by 5 digits."
        )
