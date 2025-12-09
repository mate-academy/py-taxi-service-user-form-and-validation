from django.core.exceptions import ValidationError


def validate_license_number(value: str) -> None:
    if len(value) != 8:
        raise ValidationError("License number length must be 8")
    if not value[:3].isupper() or not value[:3].isalpha():
        raise ValidationError(
            "License number first 3 characters must be uppercase"
        )
    if not value[-5:].isnumeric():
        raise ValidationError(
            "License number last 5 characters must be numeric"
        )
