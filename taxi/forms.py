from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "username",
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        return valid_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        return valid_license_number(self.cleaned_data["license_number"])


def valid_license_number(license_number: str) -> str:
    license_length = 8

    if len(license_number) != license_length:
        raise ValidationError(
            "Ensure that the license number "
            f"is {license_length} characters"
        )
    if not (license_number[:3].isalpha() and license_number[:3].isupper()):
        raise ValidationError(
            "The first three characters must be capital letters"
        )
    if not license_number[3:].isdigit():
        raise ValidationError(
            "The last 5 characters must be a number"
        )

    return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Driver
        fields = "__all__"
