import string
from django.core.exceptions import ValidationError


def license_number_validator(license_number):
    if len(license_number) != 8:
        raise ValidationError("License number must contain 8 characters.")

    test_list = [
        [set(string.ascii_uppercase), license_number[0:3]],
        [set(string.digits), license_number[3:8]]
    ]
    for allowed_set, segment in test_list:
        for character in segment:
            if character not in allowed_set:
                raise ValidationError("Wrong format of license number.")

    return license_number
