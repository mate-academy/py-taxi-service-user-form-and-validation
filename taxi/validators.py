from django.core.exceptions import ValidationError


def validate_driver_license(value):
    if len(value) != 8:
        raise ValidationError("License number must be 8 characters long.")

    first = value[:3]
    last = value[3:]

    if not first.isalpha() or not first.isupper():
        raise ValidationError(
            "First 3 characters must be uppercase letters."
        )

    if not last.isdigit():
        raise ValidationError(
            "Last 5 characters must be digits."
        )
