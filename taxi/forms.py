from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Car

User = get_user_model()


def validate_license(license_number: str) -> str:
    if len(license_number) != 8:
        raise ValidationError("License must have 8 characters")

    if (
        not license_number[:3].isalpha()
        or not license_number[:3].isupper()
    ):
        raise ValidationError("First 3 must be uppercase letters")

    if not license_number[3:].isdigit():
        raise ValidationError("Last 5 must be digits")

    return license_number


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(max_length=8)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self) -> str:
        return validate_license(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        return validate_license(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
