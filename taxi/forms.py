from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Driver, Car
from django import forms
import re


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        pattern = r"^[A-Z]{3}\d{5}$"

        if not re.fullmatch(pattern, license_number):
            raise forms.ValidationError(
                "The license number must contain exactly 8 characters: "
                "the first 3 must be uppercase letters (A-Z), "
                "and the last 5 must be digits (0-9)."
            )
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number", ]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        pattern = r"^[A-Z]{3}\d{5}$"

        if not re.fullmatch(pattern, license_number):
            raise forms.ValidationError(
                "The license number must contain exactly 8 characters: "
                "the first 3 must be uppercase letters (A-Z), "
                "and the last 5 must be digits (0-9)."
            )
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
