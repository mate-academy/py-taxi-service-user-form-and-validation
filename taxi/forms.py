from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(license_number: str) -> str:
    prefix = license_number[:3]
    if (
        len(license_number) != 8
        or not prefix.isalpha()
        or not prefix.isupper()
        or not license_number[3:].isdigit()
    ):
        raise ValidationError(
            "Ensure that license number must consist of 8 characters:"
            " first 3 characters are uppercase letters"
            " and last 5 are digits!"
        )
    return license_number


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = (
            "model",
            "manufacturer",
            "drivers",
        )


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)
