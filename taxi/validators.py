from django.core.exceptions import ValidationError


def validate_upper_case(value):
    if not value[0:3] == value[0:3].upper() or not value[0:3].isalpha():
        raise ValidationError(
            "First three symbols must be in uppercase letters."
        )


def validate__digits(value):
    for char in value[3:]:
        if not char.isdigit():
            raise ValidationError(
                "The last 5 symbols must be digits."
            )


def validate_length(value):
    if len(value) != 8:
        raise ValidationError(
            "The length of a license must be 8 characters long."
        )
