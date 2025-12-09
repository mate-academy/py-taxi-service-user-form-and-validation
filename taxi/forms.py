from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
import re


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.fullmatch(r"[A-Z]{3}\d{5}", license_number):
            raise forms.ValidationError(
                "License number must consist of 8 characters: "
                "first 3 uppercase letters and last 5 digits."
            )
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.fullmatch(r"[A-Z]{3}\d{5}", license_number):
            raise forms.ValidationError(
                "License number must consist of 8 characters: "
                "first 3 uppercase letters and last 5 digits."
            )
        return license_number
