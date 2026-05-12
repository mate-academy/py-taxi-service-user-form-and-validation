from django import forms


def validate_license_number(license_number):

    if len(license_number) == 8:
        if all([element.isupper() for element in license_number[:3]]) and all(
                [element.isdigit() for element in license_number[3::]]):
            return license_number

    raise forms.ValidationError("Invalid input. Please consider that license "
                                "number must be consisted of:\n"
                                "1)Only 8 characters\n"
                                "2)First 3 characters are uppercase letters\n"
                                "3)Last 5 characters are digits")
