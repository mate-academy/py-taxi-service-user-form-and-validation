import re

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from taxi.models import Driver, Car


def validate_driver_license_number(func):
    def wrapper(self, *args, **kwargs):
        license_number = func(self, *args, **kwargs)
        if not re.fullmatch(r"[A-Z]{3}\d{5}", license_number):
            raise ValidationError(
                "License number must be exactly 8 characters:"
                "first 3 uppercase letters and last 5 digits."
            )
        return license_number

    return wrapper


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    @validate_driver_license_number
    def clean_license_number(self):
        return self.cleaned_data["license_number"]


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    @validate_driver_license_number
    def clean_license_number(self):
        return self.cleaned_data["license_number"]


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
