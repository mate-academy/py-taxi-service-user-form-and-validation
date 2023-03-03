from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    LENGTH = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != DriverLicenseUpdateForm.LENGTH:
            raise ValidationError(
                "Driver license must consists only of 8 characters"
            )

        if not license_number[:3].isalpha():
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )

        if not license_number[-5:].isnumeric():
            raise ValidationError("Last 5 characters must be digits")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
