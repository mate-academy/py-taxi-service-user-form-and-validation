from __future__ import annotations

import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


LICENSE_PATTERN = r"^[A-Z]{3}\d{5}$"


def validate_license(value: str) -> str:
    if not re.fullmatch(LICENSE_PATTERN, value):
        raise ValidationError(
            "License must contain 3 uppercase letters and 5 digits"
        )
    return value


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self) -> str:
        return validate_license(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        return validate_license(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
