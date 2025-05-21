import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = (
            "username", "password1", "password2",
            "first_name", "last_name", "license_number"
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.fullmatch(r"[A-Z]{3}\d{5}", license_number):
            raise forms.ValidationError("Invalid license number")
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.fullmatch(r"[A-Z]{3}\d{5}", license_number):
            raise forms.ValidationError("Invalid license number")
        return license_number


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
