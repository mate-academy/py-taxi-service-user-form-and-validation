from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Car, Driver


class LicenseValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(
                "License number must be exactly 8 characters."
            )

        if (
            not license_number[:3].isalpha()
            or not license_number[:3].isupper()
        ):
            raise ValidationError(
                "First 3 characters must be uppercase letters."
            )

        if not license_number[-5:].isdigit():
            raise ValidationError(
                "Last 5 characters must be digits."
            )

        return license_number


class DriverCreationForm(
    LicenseValidationMixin,
    UserCreationForm
):
    class Meta:
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(
    LicenseValidationMixin,
    forms.ModelForm
):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
