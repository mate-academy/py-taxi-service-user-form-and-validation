import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from taxi.models import Car, Driver


class DriverLicenseUpdateForm(ModelForm):
    LICENSE_REQUIRED_LENGTH = 8

    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        start = license_number[:3]
        end = license_number[3:]

        if len(license_number) != self.LICENSE_REQUIRED_LENGTH:
            raise ValidationError(
                "License number invalid! License number "
                f"should be {self.LICENSE_REQUIRED_LENGTH} characters long."
            )
        if (not start.isalpha() or start != start.upper()
                or not end.isnumeric()):
            raise ValidationError(
                "License number invalid! Correct license number format - "
                "AAA11111 (3 uppercase letters followed by 5 digits)."
            )

        return license_number


class DriverCreationForm(UserCreationForm, DriverLicenseUpdateForm):

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
