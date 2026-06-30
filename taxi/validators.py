from django.core.exceptions import ValidationError


def validation_license(value):
    if len(value) != 8:
        raise ValidationError("Length must be equal 8 elements")
    if not value[0:3].isalpha() or not value[0:3].isupper():
        raise ValidationError("First 3 characters must be uppercase letters")
    if not value[3:8].isdigit():
        raise ValidationError("Last 5 characters must be digits")
    return value
