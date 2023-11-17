from django.core.exceptions import ValidationError


def license_number_validator(license_number: str) -> None:
    if (len(license_number) != 8
            or not (license_number[:3].isupper()
                    and license_number[:3].isalpha())
            or not license_number[3:].isnumeric()):
        raise ValidationError(
            """License number must:
            *Consist only of 8 characters
            *First 3 characters are uppercase letters
            *Last 5 characters are digits"""
        )
