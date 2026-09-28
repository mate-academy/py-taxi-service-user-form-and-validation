import re

from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car, Driver


def validate_license_number(license_number):
    if not re.fullmatch(r"[A-Z]{3}[0-9]{5}", license_number):
        raise forms.ValidationError(
            "License number must contain exactly 8 characters: "
            "3 uppercase English letters followed by 5 digits. "
            "For example: ABC12345."
        )

    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        return validate_license_number(
            self.cleaned_data["license_number"]
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        return validate_license_number(
            self.cleaned_data["license_number"]
        )


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
