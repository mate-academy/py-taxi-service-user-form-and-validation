from django.core.exceptions import ValidationError


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError("Must consist only of 8 characters")

    for char in license_number[:3]:
        if char.islower() or not char.isalpha():
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )

    for char in license_number[-5::]:
        if not char.isdigit():
            raise ValidationError("Last 5 characters must be digits")

    return license_number
