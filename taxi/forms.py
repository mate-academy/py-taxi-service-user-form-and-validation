from django import forms
from taxi.models import Driver, Car
import re
from django.contrib.auth.forms import UserCreationForm


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.fullmatch(r"[A-Z]{3}[0-9]{5}", license_number):
            raise forms.ValidationError(
                "License must be 8 characters:"
                " 3 uppercase letters followed by 5 digits."
            )
        return license_number


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple()
        }


class DriverUserCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "license_number"
        ]
