import re

from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if not license_number:
            raise ValidationError("License number is required.")

        if not re.fullmatch(r"[A-Z]{3}\d{5}", license_number):
            raise ValidationError(
                "License must be 8 characters long: "
                "first 3 uppercase letters, last 5 digits."
            )

        return license_number


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
