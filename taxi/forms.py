import re
from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

from taxi.models import Car, Driver


def validate_license_number(license_number: Any) -> None:
    license_number_pattern = r"^[A-Z]{3}\d{5}$"
    if not re.match(license_number_pattern, license_number):
        raise forms.ValidationError("Incorrect license number")
    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self) -> None:
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number", )

    def clean_license_number(self) -> None:
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
