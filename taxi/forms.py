import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Car

User = get_user_model()

LICENSE_REGEX = r"[A-Z]{3}\d{5}"


class BaseDriverForm(forms.ModelForm):

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not re.fullmatch(LICENSE_REGEX, license_number):
            raise forms.ValidationError(
                "License number must have format: XXXDDDD"
            )

        return license_number


class DriverForm(BaseDriverForm):

    class Meta:
        model = User
        fields = "__all__"


class DriverLicenseUpdateForm(BaseDriverForm):

    class Meta:
        model = User
        fields = ("license_number",)


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "email",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not re.fullmatch(LICENSE_REGEX, license_number):
            raise forms.ValidationError(
                "License number must have format: XXXDDDD"
            )

        return license_number


class CarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
