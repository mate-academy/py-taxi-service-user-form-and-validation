import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car

Driver = get_user_model()
LICENSE_PATTERN = re.compile(r"^[A-Z]{3}\d{5}$")


class LicenseNumberValidationMixin:
    cleaned_data: dict

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if not license_number:
            return license_number

        pattern = r"^[A-Z]{3}\d{5}$"
        if not re.match(pattern, license_number):
            raise forms.ValidationError(
                "License must consist of 8 characters: "
                "first 3 characters must be uppercase letters, "
                "and the last 5 characters must be digits."
            )
        return license_number


class DriverCreationForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
