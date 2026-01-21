from django.core.exceptions import ValidationError


def validate_license_number(license_number: str) -> str:
    if len(license_number) != 8:
        raise ValidationError("Ensure that value length is equal 8")
    if not (license_number[:3].isalpha() and license_number[:3].isupper()):
        raise ValidationError(
            "Ensure that the first 3 chars are letters and uppercase"
        )
    if not license_number[3:8].isdigit():
        raise ValidationError("Ensure that the last 5 chars are digits")
    return license_number
