import re

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


Driver = get_user_model()


def validate_license_number(value: str) -> None:

    if not re.fullmatch(r"[A-Z]{3}[0-9]{5}", value):
        raise ValidationError(
            "License number must contain 3 uppercase letters "
            "followed by 5 digits."
        )


class DriverCreateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = (
            "username",
            "password",
            "first_name",
            "last_name",
            "license_number",
        )
        widgets = {
            "password": forms.PasswordInput(),
        }

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number
