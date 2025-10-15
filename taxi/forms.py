from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from taxi.models import Car

User = get_user_model()


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "license_number",
            "first_name",
            "last_name",
            "email"
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not license_number:
            raise forms.ValidationError("License is required")

        if len(license_number) != 8:
            raise forms.ValidationError("License must be exactly 8 characters")

        if (
                not license_number[:3].isalpha()
                or not license_number[:3].isupper()
        ):
            raise forms.ValidationError(
                "First 3 characters must be uppercase letters")

        if not license_number[3:].isdigit():
            raise forms.ValidationError("Last 5 characters must be digits")

        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not license_number:
            raise forms.ValidationError("License is required")

        if len(license_number) != 8:
            raise forms.ValidationError("License must be exactly 8 characters")

        if (
                not license_number[:3].isalpha()
                or not license_number[:3].isupper()
        ):
            raise forms.ValidationError(
                "First 3 characters must be uppercase letters")

        if not license_number[3:].isdigit():
            raise forms.ValidationError("Last 5 characters must be digits")

        return license_number


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple()
        }
