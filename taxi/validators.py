from django.core.exceptions import ValidationError


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError("License number must be 8 characters long!")
    elif not license_number[0:3].isalpha():
        raise ValidationError("First 3 characters must be letters!")
    elif not license_number[0:3].isupper():
        raise ValidationError("First 3 characters must be capital letters!")
    elif not license_number[3:8].isdigit():
        raise ValidationError("Last 5 characters must be digits!")
