from django import forms
from django.core.exceptions import ValidationError


class LicenseValidationMixin(forms.ModelForm):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        letter = license_number[:3]
        number = license_number[3:]
        if len(license_number) != 8:
            raise ValidationError("License number must contain exactly 8 characters")

        if not letter.isupper() or not letter.isalpha():
            raise ValidationError("First 3 characters are uppercase letters")

        if not number.isdigit():
            raise ValidationError("Last 5 characters are digits")

        return license_number
