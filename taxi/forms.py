import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


def for_clean_license_number(cleaned_data: str) -> str:
    license_number = cleaned_data

    if len(license_number) != 8:
        raise forms.ValidationError("Consist only of 8 characters")

    if not re.match(r"^[A-Z]{3}", license_number):
        raise forms.ValidationError(
            "First 3 characters are uppercase letters. For example: ABC*****"
        )

    if not re.match(r"^[A-Z]{3}\d*$", license_number):
        raise forms.ValidationError(
            "Last 5 characters are digits. For example: ***12325"
        )

    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        return for_clean_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        return for_clean_license_number(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
