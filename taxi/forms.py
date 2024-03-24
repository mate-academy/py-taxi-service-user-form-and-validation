from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def clean_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError(
            "The field must consist of exactly 8 characters."
        )
    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError(
            "The first 3 characters must be uppercase letters."
        )
    if not license_number[3:].isdigit():
        raise ValidationError(
            "The last 5 characters must be digits."
        )
    return license_number


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        validators=[clean_license_number]
    )

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[clean_license_number]
    )

    class Meta:
        model = Driver
        fields = ("license_number", )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
