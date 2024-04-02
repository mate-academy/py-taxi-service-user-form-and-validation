from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


def validator_license_number(value):

    if not (value[:3].isupper() and value[:3].isalpha()):
        raise ValidationError(
            "First 3 characters must be uppercase letters"
        )
    if not value[-5:].isdigit():
        raise ValidationError(
            "Last 5 characters must be digits"
        )
    if len(value) != 8:
        raise ValidationError(
            "Consist only of 8 characters"
        )
    return value


class DriverLicenseUpdateForm(forms.ModelForm):

    license_number = forms.CharField(
        max_length=8,
        required=True,
        validators=[validator_license_number]
    )

    class Meta:
        model = Driver
        fields = ("license_number", )


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        required=True,
        validators=[validator_license_number]
    )

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Car
        fields = "__all__"
