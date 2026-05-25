import re
from django.core.exceptions import ValidationError


def validate_license_number(value):
    if not re.match(r"^[A-Z]{3}\d{5}$", value):
        raise ValidationError(
            "License must be 3 uppercase letters and 5 digits (e.g. ABC12345)"
        )
