from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver


class LicenseNumberValidationMixin:
    @staticmethod
    def license_number_validator(license_number):
        if (
            len(license_number) != 8
            or not
               (license_number[:3].isalpha() and license_number[:3].isupper())
            or not license_number[-5:].isdigit()
        ):
            raise ValidationError("Invalid license number")
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return (
            LicenseNumberValidationMixin.
            license_number_validator(license_number)
        )


class DriverCreateForm(UserCreationForm):

    class Meta:
        model = Driver
        fields = (
            UserCreationForm.Meta.fields
            + ("first_name", "last_name", "license_number", )
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return (LicenseNumberValidationMixin.
                license_number_validator(license_number))
