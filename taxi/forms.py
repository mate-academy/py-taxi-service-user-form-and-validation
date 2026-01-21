from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Car

Driver = get_user_model()


def validate_license_number(value: str) -> str:
    if len(value) != 8:
        raise forms.ValidationError(
            "License number must contain exactly 8 characters"
        )

    prefix = value[:3]
    suffix = value[3:]

    if not prefix.isalpha() or not prefix.isupper():
        raise forms.ValidationError(
            "First 3 characters must be uppercase letters"
        )

    if not suffix.isdigit():
        raise forms.ValidationError(
            "Last 5 characters must be digits"
        )

    return value


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number")

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
