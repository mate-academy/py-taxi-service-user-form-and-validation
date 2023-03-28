from django.core.exceptions import ValidationError


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError(
            "License number must consist only of 8 characters."
        )
    if not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError(
            "First 3 characters of licence number must be uppercase letters."
        )
    if not license_number[3:8].isdigit():
        raise ValidationError("Last 5 characters must be digits.")

    return license_number
