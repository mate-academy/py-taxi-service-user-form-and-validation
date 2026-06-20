import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .models import Car

User = get_user_model()


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError(
            "License number must consist of 8 characters."
        )

    if not re.fullmatch(r"[A-Z]{3}[0-9]{5}", license_number):
        raise ValidationError(
            "License number must start with 3 uppercase letters "
            "and end with 5 digits."
        )


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number],
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
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
        model = User
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
