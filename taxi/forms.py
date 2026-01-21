from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Driver, Car


def validate_license_number(license_number: str):
    if len(license_number) != 8:
        raise ValidationError("License must be exactly 8 characters long.")

    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError("First 3 characters must be uppercase letters.")

    if not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits.")

    return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        return validate_license_number(license_number)


class DriverCreateForm(UserCreationForm):
    class Meta(DriverLicenseUpdateForm.Meta):
        model = Driver
        fields = [
            "username",
            "first_name",
            "last_name",
            "license_number",
            "password"
        ]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        return validate_license_number(license_number)


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            "model",
            "manufacturer",
            "drivers"
        ]

    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
