from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple

from .models import Driver, Car
import re


def validate_license_number(value):
    if not re.fullmatch(r"[A-Z]{3}\d{5}", value):
        raise ValidationError(
            "License number must have 3 uppercase"
            " letters followed by 5 digits (e.g., ABC12345)."
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number],
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Driver
        fields = ["license_number"]


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": CheckboxSelectMultiple(),
        }

class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(max_length=8, required=True, label="License Number")

    class Meta:
        model = Driver
        fields = ['username', 'first_name', 'last_name', 'email', 'license_number']