from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver


def validate_license_number(value):
    license_number = value

    if len(license_number) != 8:
        raise ValidationError(
            "License_number should consist only of 8 characters"
        )
    if not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError(
            "First 3 characters of license_number should be uppercase letters"
        )
    if not license_number[3:].isdigit():
        raise forms.ValidationError("Last 5 characters must be digits.")
    return license_number


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number]
    )

    class Meta:
        model = Driver
        fields = ["license_number"]
