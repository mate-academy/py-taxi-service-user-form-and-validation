import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import CheckboxSelectMultiple

from .models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        pattern = r"^[A-Z]{3}[0-9]{5}$"

        if not re.fullmatch(pattern, license_number):
            raise forms.ValidationError(
                "License number must consist of 3 uppercase "
                "letters and 5 digits"
            )

        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        pattern = r"^[A-Z]{3}[0-9]{5}$"

        if not re.fullmatch(pattern, license_number):
            raise forms.ValidationError(
                "License number must consist of 3 uppercase "
                "letters and 5 digits"
            )

        return license_number


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": CheckboxSelectMultiple(),
        }
