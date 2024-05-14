from django import forms


def is_valid_license(license_number):
    if len(license_number) != 8:
        raise forms.ValidationError("License Number must be 8 characters")

    if not all(char.isupper() for char in license_number[:3]):
        raise forms.ValidationError(
            "The first three characters must be in uppercase letters."
        )

    if not all(char.isdigit() for char in license_number[-5:]):
        raise forms.ValidationError("Last 5 characters must be numbers.")
    return license_number
