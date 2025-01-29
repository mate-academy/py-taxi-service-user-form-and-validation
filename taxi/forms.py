from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.core.validators import (
    RegexValidator,
    MaxLengthValidator,
    MinLengthValidator,
)

from taxi.models import Driver, Car, Manufacturer


LICENSE_LENGTH = 8

license_number_validators = [
    MinLengthValidator(LICENSE_LENGTH),
    MaxLengthValidator(LICENSE_LENGTH),
    RegexValidator(regex=r"^[A-Z]{3}[0-9]{5}$")
]


class DriverCreateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=license_number_validators,
    )

    class Meta:
        model = Driver
        fields = "__all__"


class DriverLicenseUpdateForm(UserChangeForm):
    license_number = forms.CharField(
        required=True,
        validators=license_number_validators,
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
