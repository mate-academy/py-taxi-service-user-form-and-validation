import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Car


User = get_user_model()


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError("License must be 8 characters long.")
    if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
        raise ValidationError(
            "License must start with 3 uppercase letters"
            " followed by 5 digits.")
    return license_number


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8, validators=[validate_license_number])

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["manufacturer", "drivers"]
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)
