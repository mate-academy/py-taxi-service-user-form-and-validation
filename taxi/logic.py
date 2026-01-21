from django.core.exceptions import ValidationError

LICENSE_PLATE_LENGTH = 8


def licence_number_validation(license_number: str):
    if len(license_number) != LICENSE_PLATE_LENGTH:
        raise ValidationError(
            f"License number should be "
            f"{LICENSE_PLATE_LENGTH} symbols"
        )

    if not license_number[:3].isupper():
        raise ValidationError("First 3 characters should be capitalized")

    if not license_number[:3].isalpha():
        raise ValidationError("First 3 characters should be letters")

    if not license_number[-5:len(license_number):1].isdigit():
        raise ValidationError("Last 5 characters should be digits")

    return license_number
