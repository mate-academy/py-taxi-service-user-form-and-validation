from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError("License number must be 8 characters long!")

    if not (
            license_number[:3].isalpha()
            and license_number[:3] == license_number[:3].upper()
    ):
        raise ValidationError(
            "License number first 3 characters must be uppercase letters!"
        )

    if not license_number[3:].isnumeric():
        raise ValidationError(
            "License number last 5 characters must be digits!"
        )


class LicenseNumberValidationMixin:

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class DriverCreationForm(
    LicenseNumberValidationMixin,
    UserCreationForm
):
    class Meta:
        model = Driver
        fields = [
            "username",
            "license_number",
            "first_name",
            "last_name",
            "email",
        ]


class DriverLicenseUpdateForm(
    LicenseNumberValidationMixin,
    forms.ModelForm
):
    class Meta:
        model = Driver
        fields = ["license_number"]


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
