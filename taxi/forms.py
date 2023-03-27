from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


def license_number_validator(license_number: str):
    if len(license_number) != 8:
        raise ValidationError("License must be 8 symbols")
    letters = license_number[:3]
    digits = license_number[3:]
    if not letters.isalpha() or not letters.isupper():
        raise ValidationError(
            "First 3 symbols must be uppercase letters"
        )
    if not digits.isdigit():
        raise ValidationError("Last 5 symbols must be digits")


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
        )

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        license_number_validator(license_number)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        license_number_validator(license_number)
        return license_number
