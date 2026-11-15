from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator,
)

from .models import Driver


class DriverLicenseCreateForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[
            MinLengthValidator(8),
            MaxLengthValidator(8),
            RegexValidator(
                regex="^[A-Z]{3}\\d{5}$",
                message=(
                    "License must consist of 8 characters: "
                    "3 uppercase letters followed by 5 digits (e.g.ABC12345)."
                ),
            ),
        ],
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[
            MinLengthValidator(8),
            MaxLengthValidator(8),
            RegexValidator(
                regex="^[A-Z]{3}\\d{5}$",
                message=(
                    "License must consist of 8 characters: "
                    "3 uppercase letters followed by 5 digits (e.g.ABC12345)."
                ),
            ),
        ],
    )

    class Meta:
        model = Driver
        fields = ("license_number",)
