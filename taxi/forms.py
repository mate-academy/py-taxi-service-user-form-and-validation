from string import digits

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(license_number):
    first_three_digits = license_number[:3]
    last_five_digits = license_number[3:]

    if not first_three_digits.isalpha() and not first_three_digits.isupper():
        raise ValidationError(
            "The first 3 digits of the license "
            "number must be uppercase letters."
        )
    elif not first_three_digits.isalpha():
        raise ValidationError(
            "The first 3 digits of the license number must be letters."
        )
    elif not first_three_digits.isupper():
        raise ValidationError(
            "The first 3 digits of the license number must be uppercase."
        )

    if not last_five_digits.isdigit():
        raise ValidationError(
            "The last 5 digits of the license number must be numbers."
        )

    return license_number


class DriverCreationForm(UserCreationForm):
    password1 = None
    password2 = None
    license_number = forms.CharField(max_length=8, min_length=8)

    class Meta:
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class DriverLicenseUpdateForm (forms.ModelForm):
    license_number = forms.CharField(max_length=8, min_length=8)

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
