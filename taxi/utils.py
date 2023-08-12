from django import forms


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise forms.ValidationError(
            "License number must consist of 8 characters."
        )
    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise forms.ValidationError(
            "First 3 characters must be uppercase letters."
        )
    if not license_number[3:].isdigit():
        raise forms.ValidationError(
            "Last 5 characters must be digits."
        )
