from django.core.exceptions import ValidationError


def license_number_validator(license_number: str) -> None:
    if len(license_number) != 8:
        raise ValidationError("license_number must be 8 characters long")

    if not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError("First 3 characters must be uppercase letters")

    if not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits")
