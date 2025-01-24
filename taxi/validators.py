from django.core.exceptions import ValidationError
import re


def validate_license_number(license_number):
    """
    Validates that the license_number:
    - Is exactly 8 characters long
    - Has 3 uppercase letters followed by 5 digits
    """
    if not re.fullmatch(r"^[A-Z]{3}\d{5}$", license_number):
        raise ValidationError(
            "License number must consist of 3 "
            "uppercase letters followed by 5 digits."
        )
