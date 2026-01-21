import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car

User = get_user_model()

LICENSE_RE = re.compile(r"^[A-Z]{3}\d{5}$")


def validate_license(value: str) -> str:
    value = (value or "").strip()
    if not LICENSE_RE.fullmatch(value):
        raise forms.ValidationError(
            "License must be exactly 8 characters: 3 uppercase letters followed by 5 digits (e.g. ABC12345)."
        )
    return value


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "license_number", "password1", "password2")

    def clean_license_number(self):
        value = self.cleaned_data.get("license_number")
        return validate_license(value)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("license_number",)

    def clean_license_number(self):
        value = self.cleaned_data.get("license_number")
        return validate_license(value)


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
