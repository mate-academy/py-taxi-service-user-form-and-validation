import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError("License number length must be 8")

    if not re.match("[A-Z]{3}", license_number[:3]):
        raise ValidationError(
            "First 3 characters must be uppercase letters"
        )

    if not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits")

    return license_number


class LicenseFormMixin(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        required=True,
        validators=[validate_license_number]
    )

    class Meta:
        abstract = True


class DriverCreateForm(LicenseFormMixin, UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(LicenseFormMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
