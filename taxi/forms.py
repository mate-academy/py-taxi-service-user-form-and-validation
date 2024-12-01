from django import forms
from .models import Car, Driver
from django.core.exceptions import ValidationError


class LicenseNumberValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if len(license_number) != 8:
            raise ValidationError(
                "License number must consist of exactly 8 characters."
            )
        first_three = license_number[:3]
        if not first_three.isupper() or not first_three.isalpha():
            raise ValidationError(
                "The first 3 characters must be uppercase letters."
            )
        if not license_number[3:].isdigit():
            raise ValidationError("The last 5 characters must be digits.")
        return license_number


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]


class DriverForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["username", "first_name", "last_name", "license_number"]


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]
