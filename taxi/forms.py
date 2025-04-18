from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number_format(license_number):
    if len(license_number) != 8:
        raise ValidationError("License must be exactly 8 characters long.")
    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError("First 3 characters must be uppercase letters.")
    if not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits.")


class DriverCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    license_number = forms.CharField(max_length=8, required=True)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        validate_license_number_format(license_number)

        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number_format(license_number)
        return license_number


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
