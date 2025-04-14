from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Driver, Car
import re


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be exactly 8 characters."
            )
        if not re.match(r"^[A-Z]{3}[0-9]{5}$", license_number):
            raise forms.ValidationError(
                "License must start with 3 uppercase letters "
                "followed by 5 digits."
            )
        return license_number


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = [
            "username",
            "password",
            "license_number",
            "first_name",
            "last_name",
        ]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be exactly 8 characters."
            )
        if not re.match(r"^[A-Z]{3}[0-9]{5}$", license_number):
            raise forms.ValidationError(
                "License must start with 3 uppercase letters "
                "followed by 5 digits."
            )
        return license_number


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
