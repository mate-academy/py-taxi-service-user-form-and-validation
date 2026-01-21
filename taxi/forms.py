from django import forms
from django.core.exceptions import ValidationError
from taxi.models import Driver, Car
import re


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(required=True)

    class Meta:
        model = Driver
        fields = ("first_name", "last_name", "license_number")

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise ValidationError(
                "License must be 8 characters: 3 uppercase letters followed by 5 digits"
            )

        return license_number




class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple()
        }