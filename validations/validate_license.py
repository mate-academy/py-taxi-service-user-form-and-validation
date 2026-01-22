from django.core.exceptions import ValidationError


def validate_license(license_number):
    if len(license_number) != 8:
        raise ValidationError(
            "The length of licence number must be equal to 8!"
        )

    first_part = license_number[:3]
    second_part = license_number[3:]

    if not (first_part.isalpha() and first_part.isupper()):
        raise ValidationError("First 3 characters must be uppercase letters")

    if not second_part.isdigit():
        raise ValidationError("Last 5 characters must be digits")

    return license_number
