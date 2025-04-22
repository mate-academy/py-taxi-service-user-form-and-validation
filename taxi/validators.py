from django.core.exceptions import ValidationError


def validate_license_number(license_number: str) -> str | None:
    if len(license_number) != 8:
        raise ValidationError(
            "The license number must consist only of 8 characters"
        )
    for character in license_number[:3]:
        if not character.isalpha() or character.islower():
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )
    for character in license_number[3:]:
        if not character.isdigit():
            raise ValidationError(
                "Last 5 characters must be digits"
            )

    return license_number
