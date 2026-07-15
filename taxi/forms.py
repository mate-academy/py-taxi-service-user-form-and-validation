from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Car


class LicenseNumberValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(
                "License number must contain exactly 8 characters."
            )

        first_three_characters = license_number[:3]
        last_five_characters = license_number[3:]

        if (
            not first_three_characters.isalpha()
            or not first_three_characters.isupper()
        ):
            raise ValidationError(
                "First 3 characters must be uppercase letters."
            )

        if not last_five_characters.isdigit():
            raise ValidationError(
                "Last 5 characters must be digits."
            )

        return license_number


class DriverCreationForm(
    LicenseNumberValidationMixin,
    UserCreationForm,
):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            "username",
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
        fields = (
            "model",
            "manufacturer",
            "drivers",
        )
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
