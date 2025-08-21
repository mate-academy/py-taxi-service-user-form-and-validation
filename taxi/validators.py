from django import forms


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise forms.ValidationError("License number "
                                    "has to be 8 characters long")
    elif not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise forms.ValidationError("First 3 characters "
                                    "have to be uppercase letters")
    elif not license_number[3:].isdigit():
        raise forms.ValidationError("Last 5 characters have to be digits")
