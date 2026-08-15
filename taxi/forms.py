import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


LICENSE_NUMBER_PATTERN = re.compile(r"[A-Z]{3}[0-9]{5}")


class LicenseNumberValidationMixin:
    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        if not LICENSE_NUMBER_PATTERN.fullmatch(license_number):
            raise ValidationError(
                "License number must contain 3 uppercase letters "
                "followed by 5 digits."
            )
        return license_number


class DriverCreationForm(
    LicenseNumberValidationMixin,
    UserCreationForm,
):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(
    LicenseNumberValidationMixin,
    forms.ModelForm,
):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {"drivers": forms.CheckboxSelectMultiple()}
