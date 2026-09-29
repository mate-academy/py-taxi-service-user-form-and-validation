from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Driver


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number")

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("License must be 8 characters")
        if (
            not license_number[:3].isupper()
            or not license_number[3:].isdigit()
        ):
            raise ValidationError("Invalid license format")
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("License must be 8 characters")

        if (
            not license_number[:3].isalpha()
            or not license_number[:3].isupper()
        ):
            raise ValidationError("Invalid license format")

        if not license_number[3:].isdigit():
            raise ValidationError("Invalid license format")

        return license_number
