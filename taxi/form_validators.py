from django.core.exceptions import ValidationError


def license_number_validator(license_number: str) -> None:
    if len(license_number) != 8:
        raise ValidationError("License number must contain 8 characters")

    if not (license_number[:3].isupper() and license_number[:3].isalpha()):
        raise ValidationError("Only first 3 characters should be in uppercase")

    if not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters should be a digits")
