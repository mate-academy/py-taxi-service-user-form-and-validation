from django.core.exceptions import ValidationError


MAX_DRIVER_LICENSE_NUMBER_LENGTH = 8
MIN_DRIVER_LICENSE_NUMBER_LENGTH = 8


def validate_license(value: str) -> None:
    if value[:3] != value[:3].upper() or not value[:3].isalpha():
        raise ValidationError(
            "License number must starts with 3 upper case letters"
        )

    if not value[-5:].isdigit():
        raise ValidationError(
            "License number must ends with 5 digits"
        )
