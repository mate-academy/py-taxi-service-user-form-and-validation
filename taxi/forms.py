import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


def validate_license_number(license_number: str) -> str:
    if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
        raise forms.ValidationError(
            "License must consist of 8 characters: "
            "first 3 characters must be uppercase letters, "
            "and last 5 must be digits."
        )
    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self) -> str:
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        return validate_license_number(self.cleaned_data["license_number"])
