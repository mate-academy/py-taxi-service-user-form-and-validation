from django import forms
from django.contrib.auth import get_user_model

from taxi.models import Driver, Car

from django.core.exceptions import ValidationError


def validate_license_number(value):
    license_len = 8
    num_first_upper = 3
    num_last_digits = 5
    if len(value) != license_len:
        raise ValidationError(
            f"Ensure the value consist only of {license_len} characters"
        )
    check_value = value[:num_first_upper]
    if not check_value.isalpha() or not check_value.isupper():
        raise ValidationError(
            f"Ensure the FIRST {num_first_upper} characters are "
            f"uppercase letters"
        )
    if not value[-num_last_digits:].isdigit():
        raise ValidationError(
            f"Ensure the LAST {num_last_digits} characters are digits"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[validate_license_number, ]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[validate_license_number, ]
    )

    class Meta:
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
