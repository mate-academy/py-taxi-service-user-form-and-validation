import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        licence_number = self.cleaned_data["license_number"]
        validate_license_number_format(licence_number)
        return licence_number


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number_format(license_number)
        return license_number


def validate_license_number_format(value):
    if not re.fullmatch(r"[A-Z]{3}\d{5}", value):
        raise ValidationError(
            "License number must consist of 3 "
            "uppercase letters followed by 5 digits (e.g., ABC12345)."
        )
