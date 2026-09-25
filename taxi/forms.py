import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


# class DriverCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = Driver
#         fields = UserCreationForm.Meta.fields + ("license_number", )


def validate_license_number(license_number):
    pattern = r"^[A-Z]{3}\d{5}$"

    if not re.fullmatch(pattern, license_number):
        raise ValidationError(
            "License number must contain 3 uppercase letters "
            "followed by 5 digits. Example: ABC12345."
        )

    return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
