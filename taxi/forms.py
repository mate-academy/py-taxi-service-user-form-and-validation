import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(value):
    if len(value) != 8:
        raise ValidationError(
            "License number must be exactly 8 characters long.",
            code="invalid_length"
        )
    if not re.match(r"^[A-Z]{3}", value):
        raise ValidationError(
            "The first 3 characters must be uppercase letters",
            code="invalid_first_three_characters"
        )
    if not re.search(r"\d{5}$", value):
        raise ValidationError(
            f"The last 5 characters must be numbers {value}",
            code="invalid_last_five_characters"
        )


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        validators=[validate_license_number],
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (
            "username", "first_name", "last_name", "email", "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[validate_license_number],
    )

    class Meta:
        model = Driver
        fields = ("license_number",)
