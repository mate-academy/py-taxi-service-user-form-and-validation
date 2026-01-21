from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.forms import (
    ModelMultipleChoiceField,
    ModelForm,
    CheckboxSelectMultiple
)

from taxi.models import Driver, Car


license_number_validator = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message="License number must consist "
            "of exactly 3 uppercase letters followed by 5 digits."
)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(validators=[license_number_validator])

    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must consist of exactly 8 characters."
            )
        if not (
                license_number[:3].isalpha() and license_number[:3].isupper()
        ):
            raise forms.ValidationError(
                "The first 3 characters must be uppercase letters."
            )
        if not license_number[3:].isdigit():
            raise forms.ValidationError(
                "The last 5 characters must be digits."
            )
        return license_number


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(validators=[license_number_validator])

    class Meta:
        model = Driver
        fields = [
            "username",
            "license_number",
            "first_name",
            "last_name",
            "password1",
            "password2"
        ]


class CarCreationForm(ModelForm):
    drivers = ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
