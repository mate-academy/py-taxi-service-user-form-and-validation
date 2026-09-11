from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise forms.ValidationError(
            "License number must consist of 8 characters"
        )

    if not license_number[:3].isalpha():
        raise forms.ValidationError(
            "First 3 characters must be letters"
        )

    if not license_number[:3].isupper():
        raise forms.ValidationError(
            "First 3 characters must be uppercase"
        )

    if not license_number[3:].isdigit():
        raise forms.ValidationError(
            "Last 5 characters must be digits"
        )

    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        driver_license = self.cleaned_data["license_number"]
        return validate_license_number(driver_license)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        driver_license = self.cleaned_data["license_number"]
        return validate_license_number(driver_license)


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
