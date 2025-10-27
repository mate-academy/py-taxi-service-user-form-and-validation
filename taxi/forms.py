from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Car


def license_number_validation(license_number: str):
    if (
        len(license_number) != 8
        or license_number[:3] != license_number[:3].upper()
        or not (license_number[:3].isalpha())
        or not (license_number[-5:].isnumeric())
    ):
        raise ValidationError(
            "Please, make sure that your license number: "
            "1 - Consist only of 8 characters. "
            "2 - First 3 characters are uppercase letters. "
            "3 - Last 5 characters are digits. "
        )
    return license_number


class DriverCreationForm(UserCreationForm):

    def clean_license_number(self):
        return license_number_validation(
            license_number=self.cleaned_data["license_number"]
        )

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    def clean_license_number(self):
        return license_number_validation(
            license_number=self.cleaned_data["license_number"]
        )

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = (
            "model",
            "manufacturer",
            "drivers"
        )
