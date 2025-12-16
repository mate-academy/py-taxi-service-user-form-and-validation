from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
import re

Driver = get_user_model()


def validate_license_number(value: str) -> None:
    if not re.fullmatch(r"[A-Z]{3}\d{5}", value):
        raise forms.ValidationError(
            "License must contain 8 characters: "
            "first 3 uppercase letters and last 5 digits."
        )


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(validators=[validate_license_number])

    class Meta:
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
            "password1",
            "password2",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(validators=[validate_license_number])

    class Meta:
        model = Driver
        fields = ("license_number",)
