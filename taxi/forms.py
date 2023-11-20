import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from taxi.models import Car, Driver


class DriverLicenseUpdateForm(ModelForm):
    REQUIRED_LENGTH = 8

    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        pattern = r"^[A-Z]{3}[0-9]{5}"

        if (len(license_number) != self.REQUIRED_LENGTH
                or not re.match(pattern=pattern, string=license_number)):
            raise ValidationError(
                "License number invalid! Please enter correct license number."
            )

        return license_number


class DriverCreationForm(UserCreationForm):
    REQUIRED_LENGTH = 8

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
