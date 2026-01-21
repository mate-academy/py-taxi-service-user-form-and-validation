from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Driver


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError(
                "The license number must be exactly 8 characters long."
            )

        alpha_part = license_number[:3]
        digits_part = license_number[3:]

        if not (alpha_part.isalpha() and alpha_part.isupper()):
            raise forms.ValidationError(
                "The first three characters must be uppercase letters."
            )

        if not digits_part.isdigit():
            raise forms.ValidationError(
                "The last five characters must be digits."
            )

        return license_number


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = ["username", "password1", "password2", "license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError(
                "The license number must be exactly 8 characters long."
            )

        alpha_part = license_number[:3]
        digits_part = license_number[3:]

        if not (alpha_part.isalpha() and alpha_part.isupper()):
            raise forms.ValidationError(
                "The first three characters must be uppercase letters."
            )

        if not digits_part.isdigit():
            raise forms.ValidationError(
                "The last five characters must be digits."
            )

        return license_number
