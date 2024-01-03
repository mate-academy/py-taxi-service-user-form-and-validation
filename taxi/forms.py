from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver


def validate_license_number(license_number) -> str:
    for letter in license_number[:3]:
        if letter not in "QWERTYUIOPASDFGHJKLZXCVBNM":
            raise ValidationError("Ensure the value of first"
                                  " must be 3 uppercase letter")
    for num in license_number[3:]:
        if num not in "1234567890":
            raise ValidationError("Ensure the value"
                                  " of last 5 symbols must be numbers")
    if len(license_number) != 8:
        raise ValidationError("Ensure the lenght of license number must be 8")
    return license_number


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Driver
        fields = (UserCreationForm.Meta.fields
                  + ("first_name", "last_name", "license_number"))

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])
