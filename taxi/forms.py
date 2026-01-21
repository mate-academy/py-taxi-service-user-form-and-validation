from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def valid_license_number(license_number) -> str:
    if len(license_number) != 8:
        raise ValidationError("Must consist of only 8 characters")
    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError(
            "The first 3 characters must be uppercase letters"
        )
    if not license_number[-5:].isdigit():
        raise ValidationError("Last 5 characters must be digits")
    return license_number


class DriverCreateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = (
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "license_number"
        )

    def clean_license_number(self) -> str:
        return valid_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        return valid_license_number(self.cleaned_data["license_number"])


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"

    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
