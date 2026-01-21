from django.core.exceptions import ValidationError


def validate_license_number(license_number: str):
    if len(license_number) != 8:
        raise ValidationError("License number must be 8 characters long.")
    if (
            not license_number[:3].isalpha()
            or not license_number[:3].isupper()
    ):
        raise ValidationError(
            "First 3 characters must be uppercase letters."
        )
    if not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits.")
