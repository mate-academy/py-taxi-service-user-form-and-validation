from django.core.exceptions import ValidationError


def license_number_validator(license_number: str) -> str:
    if not isinstance(license_number, str) or not license_number.isalnum():
        raise ValidationError(
            "Your license number must contain "
            "digits and upper-case latin letters."
        )

    elif len(license_number) != 8:
        raise ValidationError("Your license number must be 8 characters long.")

    elif (
        not license_number[:3].isalpha()
        or not license_number[:3].isupper()
        or not license_number[3:].isdigit()
    ):
        raise ValidationError('License number format must be: "ABC12345"')

    return license_number
