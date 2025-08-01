from django import forms
from django.core.exceptions import ValidationError
import re

from .models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        pattern = r"^[A-Z]{3}[0-9]{5}$"

        if not re.match(pattern, license_number):
            raise ValidationError(
                "License number must consist of 8 characters: "
                "first 3 uppercase letters, followed by 5 digits.")
        return license_number


class DriverCreationForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number")

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        pattern = r"^[A-Z]{3}[0-9]{5}$"
        if not re.match(pattern, license_number):
            raise ValidationError(
                "License number must consist of 8 characters: "
                "first 3 uppercase letters, followed by 5 digits."
            )
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Car
        fields = "__all__"
