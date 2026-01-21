from django.contrib.auth.forms import UserCreationForm
from .models import Driver
from django import forms
import re


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = ["username", "first_name",
                  "last_name", "license_number"]


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise forms.ValidationError(
                "License number must be 8 characters long,"
                " with the first 3 uppercase letters followed by 5 digits.")
        return license_number
