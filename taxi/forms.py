import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Car

Driver = get_user_model()


def validate_license_number(value):
    if len(value) != 8:
        raise ValidationError(
            "The license number must consist of exactly 8 characters."
        )

    if not re.match(r"^[A-Z]{3}\d{5}$", value):
        raise ValidationError("Incorrect format")

    return value


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
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
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        validate_license_number(license_number)
        return license_number


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
