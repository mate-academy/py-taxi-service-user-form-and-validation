from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Driver, Car


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
            "password"
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.fullmatch(r"[A-Z]{3}\d{5}", license_number):
            raise ValidationError(
                "License must have 3 uppercase letters followed by 5 digits."
            )
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.fullmatch(r"[A-Z]{3}\d{5}", license_number):
            raise (ValidationError("License must have "
                                   "3 uppercase "
                                   "letters followed by 5 digits."))

        return license_number


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple()
        }
