from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Car


User = get_user_model()


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]

        validate_license_number(license_number)

        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]

        validate_license_number(license_number)

        return license_number


def validate_license_number(license_number: str) -> None:
    if len(license_number) != 8:
        raise ValidationError(
            "License number must consist of 8 characters."
        )

    if not license_number[:3].isalpha():
        raise ValidationError(
            "First 3 characters must be uppercase letters."
        )

    if not license_number[:3].isupper():
        raise ValidationError(
            "First 3 characters must be uppercase letters."
        )

    if not license_number[3:].isdigit():
        raise ValidationError(
            "Last 5 characters must be digits."
        )
