from django.core.exceptions import ValidationError


def validate_license_number(value: str) -> None:
    if len(value) != 8:
        raise ValidationError("License number must be exactly 8 chars")
    if not value[:3].isalpha() or not value[:3].isupper():
        raise ValidationError("First 3 chars needs to be uppercase letters")
    if not value[3:].isdigit():
        raise ValidationError("Last 5 chars needs to be digits")
