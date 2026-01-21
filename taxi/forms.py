from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number", ]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "License must be exactly 8 characters long"
            )

        letters_part = license_number[:3]
        if not letters_part.isalpha() or not letters_part.isupper():
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )

        digits_part = license_number[3:]
        if not digits_part.isdigit():
            raise ValidationError("Last 5 characters must be digits")

        return license_number
