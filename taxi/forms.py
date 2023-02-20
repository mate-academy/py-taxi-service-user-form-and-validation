import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


def get_license_validator() -> object:
    return RegexValidator(regex=re.compile("^[A-Z]{3}[0-9]{5}$"))


class DriverForm(UserCreationForm):
    license_number = forms.CharField(
        validators=[get_license_validator()]
    )

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number", "first_name", "last_name",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[get_license_validator()]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Car
        fields = "__all__"
