from django.core.exceptions import ValidationError


def validate_license_number(license_number: str) -> ValidationError | None:
    first_3_characters = license_number[:3]
    last_5_characters = license_number[3:]

    if (
            not all(
                char.isalpha()
                and char.isupper() for char in first_3_characters
            )
    ):
        raise ValidationError(
            "First 3 characters are not valid. They must be uppercase."
        )

    if not all(char.isdigit() for char in last_5_characters):
        raise ValidationError(
            "Last 5 characters are not valid. They must be digits."
        )
