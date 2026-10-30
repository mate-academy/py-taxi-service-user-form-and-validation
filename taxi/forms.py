from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car


class LicenseNumberValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if not license_number:
            raise ValidationError("License number cannot be empty.")
        if len(license_number) != 8:
            raise ValidationError(
                "License number must be exactly 8 characters.")

        if (not license_number[:3].isalpha()
                or not license_number[:3].isupper()):
            raise ValidationError(
                "The first 3 characters must be uppercase letters.")

        if not license_number[3:].isdigit():
            raise ValidationError(
                "The last 5 characters must be digits.")

        return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverUpdateForm(forms.ModelForm, LicenseNumberValidationMixin):
    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm, LicenseNumberValidationMixin):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
        widgets = {"drivers": forms.CheckboxSelectMultiple}
