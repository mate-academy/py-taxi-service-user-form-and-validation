import re

from django.core.exceptions import ValidationError


def validation(license_number):
    if not bool(re.match(r"^[A-Z]{3}\d{5}$", license_number)):
        raise ValidationError(
            "Ensure that you entered a valid license number"
        )
    return license_number
