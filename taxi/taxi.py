from __future__ import annotations

import re

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Car, Driver


LICENSE_RE = re.compile(r"^[A-Z]{3}\d{5}$")


def validate_license_number(value: str) -> str:
    """Validate driver's license number.

    Rules:
    - exactly 8 characters
    - first 3 characters are uppercase letters
    - last 5 characters are digits
    """
    value = (value or "").strip()
    if len(value) != 8:
        raise forms.ValidationError("License number must consist of 8 characters")
    if not LICENSE_RE.match(value):
        raise forms.ValidationError(
            "License number must have 3 uppercase letters and 5 digits"
        )
    return value


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number")

    def clean_license_number(self) -> str:
        return validate_license_number(self.cleaned_data.get("license_number", ""))


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        return validate_license_number(self.cleaned_data.get("license_number", ""))


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
