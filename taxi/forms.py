from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, CheckboxSelectMultiple

from taxi.models import Driver, Car
from .validators import (
    validate_upper_case,
    validate__digits,
    validate_length,
)


class DriverCreationForm(UserCreationForm):
    license_number = CharField(
        validators=[
            validate_upper_case,
            validate__digits,
            validate_length,
        ]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "username",
            "first_name",
            "last_name",
            "license_number",
            "is_staff",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = CharField(
        validators=[
            validate_upper_case,
            validate__digits,
            validate_length,
        ],
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
