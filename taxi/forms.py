from django import forms
from .models import Driver, Car
import re

class DriverCreationForm(forms.ModelForm):
    """Form for creating a driver with license validation."""
    class Meta:
        model = Driver
        fields = ["username", "license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        pattern = r"^[A-Z]{3}\d{5}$"
        if not re.match(pattern, license_number):
            raise forms.ValidationError("License must be 3 uppercase letters followed by 5 digits.")
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    """Form for updating a driver’s license with validation."""
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        pattern = r"^[A-Z]{3}\d{5}$"
        if not re.match(pattern, license_number):
            raise forms.ValidationError("License must be 3 uppercase letters followed by 5 digits.")
        return license_number


class CarForm(forms.ModelForm):
    """Use checkboxes to assign drivers to a car."""
    class Meta:
        model = Car
        fields = ["name", "manufacturer", "drivers"]
        widgets = {
            "drivers": forms.CheckboxSelectMultiple()
        }
