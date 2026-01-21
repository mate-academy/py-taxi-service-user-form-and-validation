from django.core.exceptions import ValidationError


def custom_license_number_validator(license_number: str) -> str:
    LENGTH_OF_LICENCE_NUMBER = 8

    if len(license_number) != LENGTH_OF_LICENCE_NUMBER:
        raise ValidationError(
            f"The license number must be "
            f"{LENGTH_OF_LICENCE_NUMBER} characters long."
        )
    if not (license_number[:3].isalpha() and license_number[:3].isupper()):
        raise ValidationError(
            "The first 3 characters must be uppercase letters."
        )
    if not license_number[3:].isdigit():
        raise ValidationError(
            "Make sure the last 5 characters are numbers."
        )
    return license_number
