from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validator_license_number(value: str):
    valid_length = 8
    license_number = value
    valid_chars = license_number[:3].isalpha() and license_number[:3].isupper()
    valid_digits = license_number[3:].isdigit()

    if len(license_number) == valid_length and valid_chars and valid_digits:
        return license_number

    raise ValidationError(
        """
        The license number must be 8 characters long,
        The first 3 characters are capital letters,
        The last 5 characters are numbers,
        """
    )


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        max_length=8,
        validators=[validator_license_number]
    )

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        max_length=8,
        validators=[validator_license_number]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
