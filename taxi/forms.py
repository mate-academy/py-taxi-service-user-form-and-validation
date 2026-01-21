import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator

from taxi.models import Driver, Car


def validate_uppercase_start(value):
    if not re.match(r"^[A-Z]{3}", value):
        raise ValidationError("First 3 symbols should be uppercase letters.")


def validate_last_five_digits(value):
    str_value = str(value)
    if not re.match(r".*\d{5}$", str_value):
        raise ValidationError("Last five symbols should be an integer.")


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[
            MinLengthValidator(8),
            MaxLengthValidator(8),
            validate_uppercase_start,
            validate_last_five_digits,
        ],
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "username",
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):

    license_number = forms.CharField(
        required=True,
        validators=[
            MinLengthValidator(8),
            MaxLengthValidator(8),
            validate_uppercase_start,
            validate_last_five_digits,
        ],
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
