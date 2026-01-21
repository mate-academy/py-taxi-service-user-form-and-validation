import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Driver, Car


def validate_license_number(value):
    if not re.match(r"^[A-Z]{3}\d{5}$", value):
        raise forms.ValidationError(
            "Enter valid information about "
            "license plate (3 uppercase letters and 5 digits)"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("first_name", "last_name", "license_number",)

    def clean_license_number(self):
        clean_license_number = self.cleaned_data["license_number"]
        validate_license_number(clean_license_number)
        return clean_license_number


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = ("first_name", "last_name", "license_number",)

    def clean_license_number(self):
        clean_license_number = self.cleaned_data["license_number"]
        validate_license_number(clean_license_number)
        return clean_license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
