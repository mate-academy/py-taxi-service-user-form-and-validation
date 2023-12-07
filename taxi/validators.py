from django.core.exceptions import ValidationError


def validate_license_number(license_number: str) -> str:
    if len(license_number) != 8:
        raise ValidationError("License Number must be of length 8!")
    elif not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError(
            "License Number has to start with 3 uppercase letters!"
        )
    elif not license_number[3:].isdigit():
        raise ValidationError("License Number has to end with 5 digits!")

    return license_number
