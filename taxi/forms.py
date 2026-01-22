from django import forms
from taxi.models import Driver, Car
import re


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError("License number must be 8 characters.")
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise forms.ValidationError(
                "License number must start with 3 "
                "uppercase letters and be followed by 5 digits."
            )
        return license_number


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["model", "manufacturer"]
        widgets = {
            "drivers": forms.CheckboxSelectMultiple
        }
