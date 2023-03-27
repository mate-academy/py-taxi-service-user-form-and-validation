from django.contrib.auth.forms import (
    UserCreationForm,
    ReadOnlyPasswordHashField,
)
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver


class LicenseMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                f"You entered {len(license_number)} characters, it should be 8"
            )
        if not all(num.isdigit() for num in license_number[3:]):
            raise ValidationError("Last 5 characters should be numbers")
        if not all(letter.isalpha() for letter in license_number[0:3]):
            raise ValidationError("First 3 characters should be letters")
        if not all(letter.isupper() for letter in license_number[0:3]):
            raise ValidationError("First 3 letters should be uppercase")
        return license_number


class DriverCreationForm(UserCreationForm, LicenseMixin):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )


class DriverLicenseUpdateForm(forms.ModelForm, LicenseMixin):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number",)
