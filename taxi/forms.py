from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator
)

from .models import Driver, Car


class LicenseNumberValidationMixin:
    LICENSE_NUMBER_LENGTH = 8
    RE_LICENSE_NUMBER_START = r"\A[A-Z]{3,3}"
    RE_LICENSE_NUMBER_END = r"\d{5,5}\Z"

    license_number = forms.CharField(
        validators=[
            MinLengthValidator(LICENSE_NUMBER_LENGTH),
            MaxLengthValidator(LICENSE_NUMBER_LENGTH),
            RegexValidator(
                RE_LICENSE_NUMBER_START,
                message="First 3 characters must be letters in uppercase"
            ),
            RegexValidator(
                RE_LICENSE_NUMBER_END,
                message="Last 5 characters must be digits"
            )
        ]
    )


class DriverCreationForm(
    LicenseNumberValidationMixin,
    UserCreationForm

):
    license_number = LicenseNumberValidationMixin.license_number

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(
    LicenseNumberValidationMixin,
    forms.ModelForm,
):

    license_number = LicenseNumberValidationMixin.license_number

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):

    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
