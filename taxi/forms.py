from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from taxi.models import Driver, Car


def validate_license_number(license_number: str) -> str:
    if len(license_number) != 8:
        raise ValidationError(
            "License number must be exactly 8 characters long."
        )
    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError(
            "The first 3 characters of the license "
            "number must be uppercase letters."
        )
    if not license_number[3:8].isnumeric():
        raise ValidationError(
            "The last 5 characters of the license number must be digits."
        )

    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("username", "password1", "password2", "license_number")

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
