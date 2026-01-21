from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(license_number):
    license_number_length = 8
    if len(license_number) == license_number_length:
        if all([
            license_number[:3].isalpha(),
            license_number[:3].isupper(),
            license_number[3:].isdigit()
        ]):
            return True
    return False


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if validate_license_number(license_number):
            return license_number

        raise ValidationError(
            "License number must contains exactly 8 characters."
            "First 3 characters must be uppercase letters."
            "Last 5 characters must be digits."
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_LENGTH = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if validate_license_number(license_number):
            return license_number

        raise ValidationError(
            "License number must contains exactly 8 characters."
            "First 3 characters must be uppercase letters."
            "Last 5 characters must be digits."
        )


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer",)
