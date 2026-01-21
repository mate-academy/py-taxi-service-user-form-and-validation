from django.core.exceptions import ValidationError


def license_number_validator(license_number) -> None:
    license_length = 8

    if len(license_number) != license_length:
        raise ValidationError(
            "License number must consist only of 8 characters"
        )

    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError(
            "License number must start with 3 uppercase letters "
        )

    if not license_number[3:].isdigit():
        raise ValidationError(
            "License number must end with 5 digits"
        )
