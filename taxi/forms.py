from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxLengthValidator, MinLengthValidator

from taxi.models import Driver, Car
from taxi.validators.driver_license_validation import (
    validate_license,
    MAX_DRIVER_LICENSE_NUMBER_LENGTH,
    MIN_DRIVER_LICENSE_NUMBER_LENGTH,
)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[
            validate_license,
            MaxLengthValidator(MAX_DRIVER_LICENSE_NUMBER_LENGTH),
            MinLengthValidator(MIN_DRIVER_LICENSE_NUMBER_LENGTH),
        ]
    )

    class Meta:
        model = Driver
        fields = ("license_number", )


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        validators=[
            validate_license,
            MaxLengthValidator(MAX_DRIVER_LICENSE_NUMBER_LENGTH),
            MinLengthValidator(MIN_DRIVER_LICENSE_NUMBER_LENGTH),
        ]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name"
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
