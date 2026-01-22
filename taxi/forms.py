import re

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from taxi.models import Driver, Car
from django.contrib.auth.forms import UserCreationForm


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        validators=[RegexValidator(
            regex=r"^[A-Z]{3}\d{5}$",
            message="license number must be consist first 3 "
                    "characters are uppercase letters and last"
                    " 5 characters are digits",
            code="invalid_email")
        ]
    )

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[RegexValidator(
            regex=r"^[A-Z]{3}\d{5}$",
            message="license number must be consist first 3 "
                    "characters are uppercase letters and last"
                    " 5 characters are digits",
            code="invalid_email")
        ]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = (
            "model",
            "manufacturer",
            "drivers",
        )
