from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "license_number",)

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class LicenseNumberUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError("Ensure that the license number has length of 8.")
    if not license_number[:3].isupper():
        raise ValidationError("Ensure that first 3 characters are uppercase letters.")
    if not license_number[3:].isnumeric():
        raise ValidationError("Ensure that last 5 characters are digits.")
    return license_number
