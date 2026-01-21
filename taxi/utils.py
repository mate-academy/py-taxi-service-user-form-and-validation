from django.core.exceptions import ValidationError


def is_license_valid(license_number: str) -> str:
    if len(license_number) != 8:
        raise ValidationError("License number should contains 8 characters")

    if (not license_number[:3].isupper()
            or not license_number[:3].isalpha()):
        raise ValidationError("First 3 characters must be uppercase letters")

    if not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits")

    return license_number
