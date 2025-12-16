from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Car


User = get_user_model()


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }


def validate_license_number(license_number: str) -> str:
    if len(license_number) != 8:
        raise forms.ValidationError(
            "License must contain exactly 8 characters."
        )

    first_part = license_number[:3]
    last_part = license_number[3:]

    if not first_part.isalpha() or not first_part.isupper():
        raise forms.ValidationError(
            "First 3 characters must be uppercase letters."
        )

    if not last_part.isdigit():
        raise forms.ValidationError("Last 5 characters must be digits.")

    return license_number
