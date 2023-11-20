from django.core.exceptions import ValidationError


def license_number_validator(license_number: str) -> str:
    if len(license_number) != 8:
        raise ValidationError("License number must contain 8 characters")
    if not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError(
            "First 3 characters of your driver license"
            " must be uppercase letters"
        )
    if not license_number[-5:].isdigit():
        raise ValidationError(
            "Last 5 characters of your driver license must be digits"
        )
    return license_number
