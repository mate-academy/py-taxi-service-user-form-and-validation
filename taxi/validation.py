from django.core.exceptions import ValidationError


def validate_license(license_number: str) -> str:
    if len(license_number) != 8:
        raise ValidationError(
            "Ensure that license number has 8 characters"
        )
    if not (license_number[:3].isalpha() and license_number[:3].isupper()):
        raise ValidationError(
            "Ensure that first 3 characters are uppercase letters"
        )
    if not license_number[3:].isdigit():
        raise ValidationError(
            "Ensure that last 5 characters are digits"
        )

    return license_number
