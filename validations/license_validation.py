from django.core.exceptions import ValidationError


def validate_license_number(license_number):
    first_three_characters = license_number[:3]
    last_five_characters = license_number[-5:]

    if len(license_number) != 8:
        raise ValidationError(
            "The length of licence number must be equal to 8."
        )
    if (not first_three_characters.isupper()
            or not first_three_characters.isalpha()):
        raise ValidationError("First 3 characters must be uppercase letters.")
    if not last_five_characters.isdigit():
        raise ValidationError("Last 5 characters must be digits.")

    return license_number
