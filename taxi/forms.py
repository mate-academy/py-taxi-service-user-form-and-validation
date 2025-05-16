from curses.ascii import isupper, isdigit

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(license_number: str) -> str:
    if len(license_number) != 8:
        raise ValidationError(
            "Ensure the license number contains 8 characters"
        )
    elif not (
            license_number[:3].isalpha() and license_number[:3].isupper()
    ):
        raise ValidationError(
            "Ensure the first 3 characters are uppercase letters"
        )
    elif not license_number[-5:].isdigit():
        raise ValidationError(
            "Ensure the last 5 characters are digits"
        )
    return license_number


class DriverLicenseCreateForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = "__all__"

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
