import re

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license(license_number: str) -> None:
    if not re.match("[A-Z]{3}[0-9]{5}", license_number):
        raise ValidationError("License number must contain 8 letter in which"
                              " first 3 - is digit and last 5 is numbers.")


class LicenseFormMixin(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license],
        required=True
    )

    class Meta:
        abstract = True


class DriverCreationForm(LicenseFormMixin, UserCreationForm):
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


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Car
        fields = "__all__"
