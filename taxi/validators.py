from django.core.exceptions import ValidationError


def clean_license_number(license_number):
    len_license_number = 8

    if len(license_number) != len_license_number:
        raise ValidationError(f"Ensure the value is {len_license_number}")
    if not license_number[0:3].isupper():
        raise ValidationError(
            "Ensure the first 3 characters are uppercase letters"
        )
    if not license_number[4:].isdigit():
        raise ValidationError("last 5 characters are digits")
    return license_number
