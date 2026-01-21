from django.core.exceptions import ValidationError


def validate_license_number(value):
    if len(value) != 8:
        raise ValidationError("license number must consist of 8 characters")
    if not (value[0].isupper() and value[1].isupper() and value[2].isupper()):
        raise ValidationError("First 3 characters must be uppercase letters")
    if not value[3:8].isdecimal():
        raise ValidationError("Last 5 characters must be digits")
