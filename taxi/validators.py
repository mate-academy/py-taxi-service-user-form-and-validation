import re
from django.core.exceptions import ValidationError


def validate_license_number(value):
    pattern = r"^[A-Z]{3}\d{5}$"
    if not re.match(pattern, value):
        raise ValidationError("License number must be like AAA00000")
