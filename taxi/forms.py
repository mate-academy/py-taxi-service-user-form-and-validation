from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from taxi.models import Driver


def valid_license_number(license_number):
    if not license_number:
        raise ValidationError("License number is required.")

    if len(license_number) != 8:
        if len(license_number) < 8:
            raise ValidationError("License number is too short.")
        else:
            raise ValidationError("License number is too long.")

    if (not license_number[:3].isalpha()
            or license_number[:3] != license_number[:3].upper()):
        raise ValidationError("First 3 characters must be uppercase letters.")

    if not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits.")

    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
            "password1",
            "password2",
        )

    def clean_license_number(self):
        valid_number = valid_license_number(
            self.cleaned_data["license_number"]
        )
        return valid_number


class DriverLicenseUpdateForm(ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        valid_number = valid_license_number(
            self.cleaned_data["license_number"]
        )
        return valid_number
