from django import forms


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise forms.ValidationError("Length of license number must be 8.")
    if not (license_number[:3].isalpha() and license_number[:3].isupper()):
        raise forms.ValidationError("First 3 characters"
                                    " of license number must be uppercase.")
    if not license_number[-5:].isdigit():
        raise forms.ValidationError("Last 5 characters"
                                    " of license number must be digits.")
