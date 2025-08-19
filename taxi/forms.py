import re

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import (
    ModelForm,
    ModelMultipleChoiceField,
    CheckboxSelectMultiple
)

from taxi.models import Driver, Car


def validate_driver_license(license_number):
    pattern = r"^[A-Z]{3}\d{5}$"
    if not re.match(pattern, license_number):
        raise ValidationError(
            "License must contain 8 characters, first 3 are letters and "
            "last 5 are digits"
        )


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email", "username", "license_number")

    def clean_license_number(self):
        license_num = self.cleaned_data["license_number"]
        validate_driver_license(license_num)
        return license_num


class DriverLicenseUpdateForm(ModelForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_num = self.cleaned_data["license_number"]
        validate_driver_license(license_num)
        return license_num


class CarCreationForm(ModelForm):
    drivers = ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
