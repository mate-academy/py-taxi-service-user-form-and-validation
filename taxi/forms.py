from django import forms
from taxi.models import Driver
import re
from taxi.models import Car
from django import forms


class DriverCreateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["username", "password", "first_name", "last_name", "license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise forms.ValidationError("License number must be 3 uppercase letters followed by 5 digits.")
        return license_number

class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise forms.ValidationError(
                "License number must consist of 3 uppercase letters followed by 5 digits (e.g. ABC12345)."
            )
        return license_number


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
