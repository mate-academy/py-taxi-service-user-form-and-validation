import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(max_length=8, required=True)

    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2", "license_number")

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise forms.ValidationError(
                "License number must be 8 characters: first 3 uppercase letters, last 5 digits."
            )
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise forms.ValidationError(
                "License number must be 8 characters: first 3 uppercase letters, last 5 digits."
            )
        return license_number
