from django import forms


def validate_license_number(value: str) -> str:
    if len(value) != 8:
        raise forms.ValidationError("License number must be exactly 8 characters.")
    if not value[:3].isalpha() or not value[:3].isupper():
        raise forms.ValidationError("First 3 characters must be uppercase letters.")
    if not value[3:].isdigit():
        raise forms.ValidationError("Last 5 characters must be digits.")
    return value
