from django.core.exceptions import ValidationError


def license_number_validator(license_number: str) -> str:
    if len(license_number) != 8:
        raise ValidationError("License number should consist of 8 characters")
    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError("First 3 characters should be uppercase letters")
    if license_number[:3].isupper() and not license_number[-5:].isdigit():
        raise ValidationError("Last 5 characters should be digits")
    return license_number
