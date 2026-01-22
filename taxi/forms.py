from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import CheckboxSelectMultiple

from taxi.models import Driver, Car


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise forms.ValidationError(
            "License number must consist of 8 characters."
        )
    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise forms.ValidationError(
            "First 3 characters must be uppercase letters."
        )
    if not license_number[3:].isdigit():
        raise forms.ValidationError(
            "Last 5 characters must be digits."
        )


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class CarCreationForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": CheckboxSelectMultiple(),
        }
