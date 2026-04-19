import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car

User = get_user_model()


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("license_number",
                                                 "first_name",
                                                 "last_name",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if not re.fullmatch(r"[A-Z]{3}\d{5}", license_number):
            raise forms.ValidationError(
                "License must be 3 uppercase letters and 5 digits"
            )

        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if not re.fullmatch(r"[A-Z]{3}\d{5}", license_number):
            raise forms.ValidationError(
                "License must be 3 uppercase letters and 5 digits"
            )

        return license_number


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
