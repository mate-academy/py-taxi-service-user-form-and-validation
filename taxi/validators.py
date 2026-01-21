from django.core.exceptions import ValidationError


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError(
            "The length of the license number must be 8 characters"
        )
    elif not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError(
            "The first 3 characters must be uppercase"
        )
    elif not license_number[-5:].isdigit():
        raise ValidationError(
            "The last 5 characters must be digits"
        )
    return license_number
