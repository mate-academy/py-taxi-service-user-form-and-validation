from django.core.exceptions import ValidationError


LICENSE_NUMBER_LENGTH = 8


def validate_license_number(value):
    if len(value) != LICENSE_NUMBER_LENGTH:
        raise ValidationError(
            f"License number must be exactly "
            f"{LICENSE_NUMBER_LENGTH} characters long."
        )

    first_three = value[:3]
    if not first_three.isalpha() or not first_three.isupper():
        raise ValidationError(
            "First three characters "
            "must be uppercase letters."
        )

    last_five = value[-5:]
    if not last_five.isdigit():
        raise ValidationError("Last five characters must be digits.")
