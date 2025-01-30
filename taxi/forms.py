from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.validators import (
    RegexValidator,
    MaxLengthValidator,
    MinLengthValidator
)

from taxi.models import Driver, Car, Manufacturer


LICENSE_LENGTH = 8

regex_validator = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message=(
        "The value must start with 3 uppercase letters followed by 5 digits."
    )
)

license_number_validator = [
    MinLengthValidator(LICENSE_LENGTH),
    MaxLengthValidator(LICENSE_LENGTH),
    regex_validator
]


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=license_number_validator
    )

    class Meta:
        model = Driver
        fields = ("username", "password1", "password2", "license_number")


class DriverLicenseUpdateForm(UserChangeForm):
    license_number = forms.CharField(
        required=True,
        validators=license_number_validator
    )

    class Meta:
        model = Driver
        fields = ("license_number", )


class CarForm(forms.ModelForm):

    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
