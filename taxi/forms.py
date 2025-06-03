import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


def validate_license_number(value):
    if not re.fullmatch(r"[A-Z]{3}\d{5}", value):
        raise ValidationError(
            "License number must contain "
            "3 uppercase letters followed "
            "by 5 digits (e.g. ABC12345)."
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        label="License Number",
        max_length=8,
        validators=[validate_license_number],
        widget=forms.TextInput(attrs={"placeholder": "e.g. ABC12345"})
    )

    class Meta:
        model = Driver
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
        widgets = {
            "drivers": forms.CheckboxSelectMultiple
        }
