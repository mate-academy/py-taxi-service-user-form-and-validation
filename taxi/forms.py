from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Driver, Car
import re


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        pattern = r"^[A-Z]{3}\d{5}$"
        if not re.match(pattern, license_number):
            raise ValidationError(
                "License must consist of 3 uppercase letters "
                "followed by 5 digits (8 characters total)."
            )
        return license_number


class DriverCreateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        pattern = r"^[A-Z]{3}\d{5}$"
        if not re.match(pattern, license_number):
            raise ValidationError(
                "License must consist of 3 uppercase letters "
                "followed by 5 digits (8 characters total)."
            )
        return license_number


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
