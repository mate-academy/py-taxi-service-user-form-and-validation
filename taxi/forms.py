from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        return validate_license_number(self)


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "license_number")

    def clean_license_number(self):
        return validate_license_number(self)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"


def validate_license_number(value):
    license_number = value.cleaned_data["license_number"]

    if len(license_number) != 8:
        raise ValidationError(
            "License number must be exactly 8 characters long"
        )

    if (not license_number[:3].isalpha()
            or (license_number[:3] != license_number[:3].upper())):
        raise ValidationError(
            "First 3 characters should be uppercase letters"
        )

    if not license_number[-5:].isdigit():
        raise ValidationError(
            "Last 5 characters should be numbers"
        )

    return license_number
