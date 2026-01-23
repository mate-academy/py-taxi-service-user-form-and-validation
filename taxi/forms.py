from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from taxi.models import Car

Driver = get_user_model()


def clean_license_number(license_number: str) -> str:
    if len(license_number) != 8:
        raise ValidationError(
            "License number must contain 8 symbols"
        )

    if (
        not license_number[:3].isalpha()
        or not license_number[:3].isupper()
    ):
        raise ValidationError(
            "First 3 symbols must be only uppercase letters"
        )

    if not license_number[3:].isdigit():
        raise ValidationError(
            "Last 5 symbols must be only digits"
        )

    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (
            "username",
            "password1",
            "password2",
            "license_number"
        )

    def clean_license_number(self):
        return clean_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        return clean_license_number(self.cleaned_data["license_number"])


class CarForm(ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
