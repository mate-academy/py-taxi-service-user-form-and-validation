from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validator_license_number(value):

    if not (value[:3].isupper() and value[:3].isalpha()):
        raise ValidationError(
            "Ensure that the first 3 characters are uppercase"
        )
    if not value[-5:].isdigit():
        raise ValidationError(
            "Ensure that the last 5 characters are digits"
        )
    if len(value) != 8:
        raise ValidationError(
            "Ensure that the password consist only of 8 characters"
        )
    return value


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        required=True,
        validators=[validator_license_number]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number", "first_name", "last_name",
        )


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        required=True,
        validators=[validator_license_number]
    )

    class Meta:
        model = Driver
        fields = ("license_number", )
