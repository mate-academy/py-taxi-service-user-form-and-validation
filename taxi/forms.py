from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }


class LicenseValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "A driver's license must have exactly 8 characters."
            )
        if (
                not license_number[:3].isupper()
                or not license_number[:3].isalpha()
        ):
            raise ValidationError(
                "The first 3 characters must be capitalized."
            )
        if not license_number[3:].isdigit():
            raise ValidationError(
                "The last 5 characters must be numbers."
            )
        return license_number


class DriverCreationForm(LicenseValidationMixin, UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(LicenseValidationMixin, UserChangeForm):
    class Meta:
        model = Driver
        fields = ("license_number",)
