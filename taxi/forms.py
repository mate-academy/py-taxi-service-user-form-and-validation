from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


def clean_license_number(license_number):
    data = license_number.cleaned_data["license_number"]
    if len(data) != 8:
        raise (
            forms.ValidationError(
                "Driver's license must consist of exactly 8 characters"
            )
        )
    if not data[:3].isalpha() or not data[:3].isupper():
        raise (forms.ValidationError
               ("First 3 characters must be uppercase letters"))
    if not data[3:].isdigit():
        raise (forms.ValidationError
               ("Last 5 characters must be digits"))
    return data


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "username",
            "last_name",
            "first_name",
            "license_number",
        )

    def clean_license_number(self):
        return clean_license_number(self)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = [
            "license_number",
        ]

    def clean_license_number(self):
        return clean_license_number(self)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = ["model", "manufacturer"]
