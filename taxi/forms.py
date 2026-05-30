import re

from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car, Driver


def validate_license_number(license_number: str) -> str:
    if not re.fullmatch(r"[A-Z]{3}\d{5}", license_number):
        raise forms.ValidationError(
            "License number must contain 3 uppercase letters "
            "followed by 5 digits."
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

    def clean_license_number(self) -> str:
        return validate_license_number(
            self.cleaned_data["license_number"]
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        return validate_license_number(
            self.cleaned_data["license_number"]
        )


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
