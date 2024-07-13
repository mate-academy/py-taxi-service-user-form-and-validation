from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            return ValidationError(
                "License number have to consist of 8 characters"
            )
        if (not license_number[:3].isalpha()
                or license_number[3:] != license_number[3:].upper()):
            raise ValidationError(
                "First 3 characters of license number must be chars"
            )
        if not license_number[3:].isdigit():
            raise ValidationError(
                "Last 5 characters of license number must be digits"
            )
        return license_number


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ["drivers"]
