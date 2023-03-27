from django.core.exceptions import ValidationError


def validate_license_number(license_number):

    if len(license_number) != 8:
        raise ValidationError("License must consist of 8 characters")
    if not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError("The first three characters in the license must be uppercase letters")
    if not license_number[-5:].isdigit():
        raise ValidationError("The last five characters in the license must be digits")

    return license_number
