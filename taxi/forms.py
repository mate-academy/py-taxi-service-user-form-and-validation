from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(license_number: str):
    if len(license_number) != 8:
        raise ValidationError("License number must be a 8-digit number.")
    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError(
            "First 3 characters should be uppercase letters")
    if not license_number[3:].isdigit():
        raise ValidationError(
            "Last 5 characters should be digits")
    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = ("first_name",
                  "last_name",
                  "license_number",
                  ) + UserCreationForm.Meta.fields

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        return validate_license_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = (
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        return validate_license_number(license_number)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
