from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def driver_license_validator(value):
    if len(value) != 8:
        raise ValidationError("License number should consist of 8 characters")
    elif not value[:3].isupper() or not value[:3].isalpha():
        raise ValidationError("First 3 characters should be uppercase letters")
    elif not value[3:].isdigit():
        raise ValidationError("Last 5 characters should be digits")

    return value


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[
            driver_license_validator
        ]
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
        required=True,
        validators=[
            driver_license_validator
        ]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
