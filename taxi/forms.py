from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


User = get_user_model()


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError(
            "License number must contain exactly 8 characters."
        )

    if (
        not license_number[:3].isalpha()
        or not license_number[:3].isupper()
    ):
        raise ValidationError(
            "The first 3 characters must be uppercase letters."
        )

    if not license_number[3:].isdigit():
        raise ValidationError(
            "The last 5 characters must be digits."
        )

    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["license_number"]

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
