import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Car


def validate_license_number(value):
    if not re.fullmatch(r"[A-Z]{3}[0-9]{5}", value):
        raise ValidationError(
            "Enter 3 uppercase letters followed by 5 digits.",
            code="invalid_license_number",
        )


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number],
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number],
    )

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
