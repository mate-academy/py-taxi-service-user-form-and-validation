from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver


def validate_license_number(value):
    if len(value) != 8:
        raise ValidationError("License number must have 8 characters!")

    if not value[:3].isalpha():
        raise ValidationError("First 3 characters must be letters!")

    if not value[:3].isupper():
        raise ValidationError("First 3 characters must be uppercase letters!")

    if not value[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits!")


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number
