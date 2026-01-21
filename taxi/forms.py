from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise forms.ValidationError(
            "License number must be exactly 8 characters long."
        )

    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise forms.ValidationError(
            "The first 3 characters must be uppercase letters."
        )

    if not license_number[-5:].isdigit():
        raise forms.ValidationError("The last 5 characters must be digits.")

    return license_number


class DriverCreationForm(UserCreationForm):

    class Meta:
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "license_number"
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name",
            "password",
            "license_number"
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)
