from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(license_number: str) -> str:
    if len(license_number) != 8:
        raise ValidationError(
            "Ensure that length of password is exactly 8 characters"
        )
    if not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError(
            "Ensure that first three characters are letters in upper case"
        )
    if not license_number[3:].isnumeric():
        raise ValidationError(
            "Ensure that last 5 characters are digits"
        )
    return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverCreateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = "__all__"

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
