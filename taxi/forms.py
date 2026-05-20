from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Car, Driver


def validate_license_number(value):
    if len(value) != 8:
        raise forms.ValidationError(
            "License number must be exactly 8 characters."
        )
    if not value[:3].isupper() or not value[:3].isalpha():
        raise forms.ValidationError(
            "First 3 characters must be uppercase letters."
        )
    if not value[3:].isdigit():
        raise forms.ValidationError("Last 5 characters must be digits.")


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number"
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
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
            "drivers": forms.CheckboxSelectMultiple
        }
