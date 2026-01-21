from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver


def validate_license_number(license_number):
    if (
        license_number[:3].isalpha()
        and license_number[:3].isupper()
        and len(license_number) == 8
        and license_number[3:].isdigit()
    ):
        return license_number
    raise ValidationError(
        "Your license number should be 8 characters long. "
        "3 first characters should be uppercased letters. "
        "The last 5 characters should be numbers."
    )


class DriverForm(UserCreationForm):

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])

    class Meta:
        model = Driver
        fields = ("license_number",)
