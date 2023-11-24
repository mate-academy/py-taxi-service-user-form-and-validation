from django.core.exceptions import ValidationError


def license_number_validator(license_number: str) -> None:
    if len(license_number) != 8:
        raise ValidationError(
            "License number must contain 8 characters"
        )

    if not (license_number[:3].isupper() and license_number[:3].isalpha()):
        raise ValidationError(
            "License number must start with 3 uppercase letters"
        )

    if not license_number[3:].isdigit():
        raise ValidationError(
            "License number must end with 5 digits"
        )
