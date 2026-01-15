import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


def validate_license_number(license_number):
    """
    Validate license number format: AAA12345
    - First 3 characters must be uppercase letters
    - Last 5 characters must be digits
    """
    if len(license_number) != 8:
        raise ValidationError(
            "License number must be exactly 8 characters long"
        )

    if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
        raise ValidationError(
            "License number must consist of 3 uppercase letters "
            "followed by 5 digits (e.g., ABC12345)"
        )


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        validate_license_number(license_number)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        validate_license_number(license_number)
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
