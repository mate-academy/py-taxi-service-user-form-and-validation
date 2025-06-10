from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver

class DriverForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license-number",
            "first_name",
            "last_name",
        )

class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError("License number must be 8 digits")
    elif not license_number[:3].isupper() or not license_number[:3].isalhpa():
        raise ValidationError("First 3 characters should be uppercase letters")
    elif not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters should be digits")

    return license_number
