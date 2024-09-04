from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
import re

from taxi.models import Driver, Car


def validate_license_number(license_number):
    if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
        raise ValidationError(
            "License number must consist of 8 characters: "
            "the first 3 uppercase letters and the last 5 digits."
        )


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        validate_license_number(license_number)
        return license_number


class DriverLicenseUpdateForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        validate_license_number(license_number)
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
