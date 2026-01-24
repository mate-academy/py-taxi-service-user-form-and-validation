import re

from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car, Driver

_LICENSE_RE = re.compile(r"^[A-Z]{3}\d{5}$")


def validate_license_number(value: str) -> str:
    value = (value or "").strip()

    if len(value) != 8:
        raise forms.ValidationError("License number must consist of 8 characters")

    if not _LICENSE_RE.match(value):
        raise forms.ValidationError(
            "License number must have 3 uppercase letters and 5 digits"
        )

    return value


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number")

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data.get("license_number", "")
        return validate_license_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data.get("license_number", "")
        return validate_license_number(license_number)


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
