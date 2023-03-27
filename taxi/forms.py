from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        license_number_validator(license_number)
        return license_number


def license_number_validator(license_number: str):
    if len(license_number) != 8:
        raise ValidationError(
            "Ensure that length license_number is 8"
        )
    if not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError("Ensure first 3 letters are in uppercase")
    if not license_number[3:].isdigit():
        raise ValidationError("Ensure last 5 letters are only digits")


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number"
        )

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        license_number_validator(license_number)
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
