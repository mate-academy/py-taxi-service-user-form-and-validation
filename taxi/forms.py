from django.core.exceptions import ValidationError

import re

from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model

from .models import Car, Manufacturer

User = get_user_model()


def validate_license_number(value: str):
    if value is None:
        raise forms.ValidationError("License number is required.")
    if len(value) != 8:
        raise forms.ValidationError(
            "License number must be exactly 8 characters."
        )
    first3 = value[:3]
    last5 = value[3:]
    if not (first3.isalpha() and first3.isupper()):
        raise forms.ValidationError(
            "First 3 characters must be uppercase letters."
        )
    if not last5.isdigit():
        raise forms.ValidationError("Last 5 characters must be digits.")


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8, validators=[validate_license_number])

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
            "email",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise ValidationError(
                "License number must have 3 "
                "uppercase letters followed by 5 digits"
            )
        return license_number


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
