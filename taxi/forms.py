from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

import re

from taxi.models import Driver, Car


def validate_license(license_number):
    if not re.fullmatch(r"[A-Z]{3}\d{5}", license_number):
        raise ValidationError(
            "The license must consist of 3 capital letters and 5 numbers."
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[validate_license]
    )

    class Meta:
        model = Driver
        fields = ["license_number"]


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        validators=[validate_license]
    )

    class Meta:
        model = Driver
        fields = ["username", "first_name", "last_name", "license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
