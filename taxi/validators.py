from django.core.exceptions import ValidationError


def validate_license_number(value):
    if len(value) != 8:
        raise ValidationError(
            "License number must be exactly 8 characters long."
        )
    if not value[:3].isalpha():
        raise ValidationError("License number must start with 3 letters.")
    if not value[-5:].isdigit():
        raise ValidationError("License number must end with 5 digits.")
