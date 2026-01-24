import re
from django import forms


def validate_license_number(value):
    if not re.fullmatch(r"[A-Z]{3}\d{5}", value):
        raise forms.ValidationError(
            "License number must contain 3 uppercase letters "
            "followed by 5 digits."
        )
