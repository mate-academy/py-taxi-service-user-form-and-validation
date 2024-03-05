from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(value: str):
    if len(value) != 8:
        raise ValidationError("Must be only 8 characters")
    if not (value[:3].isalpha() and value[:3].isupper()):
        raise ValidationError("First 3 characters must be uppercase letters")
    if not value[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits")


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        required=True,
        validators=[validate_license_number])

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number")


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        required=True,
        validators=[validate_license_number])

    class Meta:
        model = Driver
        fields = ["license_number", ]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Car
        fields = "__all__"
