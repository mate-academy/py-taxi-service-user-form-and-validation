from django.core.exceptions import ValidationError


def validate_license_number(license_number):
    uppercase_letters = license_number[:3]
    if len(license_number) != 8:
        raise ValidationError("Ensure the value length is 8")
    if not (uppercase_letters.isalpha() and uppercase_letters.isupper()):
        raise ValidationError("Ensure that first 3 characters "
                              "are upper letters")
    if not license_number[3:].isdigit():
        raise ValidationError("Ensure that last 5 characters are digits")
    return license_number
