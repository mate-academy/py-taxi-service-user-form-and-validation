
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
import re

from taxi.models import Car

Driver = get_user_model()


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number", "")
        pattern = r"^[A-Z]{3}\d{5}$"
        if not re.match(pattern, license_number):
            raise forms.ValidationError(
                "License number must be 8 characters: first 3 "
                "uppercase letters and last 5 digits."
            )
        return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number")

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number", "")
        pattern = r"^[A-Z]{3}\d{5}$"
        if not re.match(pattern, license_number):
            raise forms.ValidationError(
                "License number must be 8 characters: "
                "first 3 uppercase letters and last 5 digits."
            )
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
