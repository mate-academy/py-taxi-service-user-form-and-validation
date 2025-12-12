import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(license_number: str) -> None:
    """
        Validates driver license number:
        - exactly 8 characters
        - first 3 uppercase letters
        - last 5 digits
        """
    pattern = r"^[A-Z]{3}\d{5}$"
    if not re.match(pattern, license_number):
        raise ValidationError(
            "License number must be exactly 8 characters: "
            "first 3 uppercase letters, then 5 digits."
        )


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
            "email"
        )

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
