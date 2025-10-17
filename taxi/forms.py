import re

from django import forms
from taxi.models import Car
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple
from django.contrib.auth import get_user_model
User = get_user_model()


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        regex = r"^[A-Z]{3}\d{5}$"
        if not re.match(regex, license_number):
            raise ValidationError("The number is not valid")
        else:
            return license_number


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
        widgets = {"drivers": CheckboxSelectMultiple()}
