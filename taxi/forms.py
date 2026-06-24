from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Car

User = get_user_model()


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise forms.ValidationError("Must Consist only of 8 characters")

    letters = license_number[:3]
    numbers = license_number[3:]

    if not letters.isalpha() or not letters.isupper():
        raise forms.ValidationError(
            "First 3 characters must be uppercase letters"
        )

    if not numbers.isdigit():
        raise forms.ValidationError(
            "Last 5 characters must be digits"
        )


class DriverForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


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
            "drivers": forms.CheckboxSelectMultiple,
        }
