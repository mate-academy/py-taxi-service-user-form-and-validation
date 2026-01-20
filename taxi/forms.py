from django import forms
from django.core.exceptions import ValidationError
from taxi.models import Driver, Car
import re


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not re.fullmatch(r"[A-Z]{3}\d{5}", license_number):
            raise ValidationError(
                "License number must consist of 3 uppercase letters followed by 5 digits."
            )

        return license_number
