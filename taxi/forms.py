import re

from django import forms
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


class DriverLicenseForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}\d{5}$",
                message=(
                    "The license number must consist of 8 characters: "
                    "the first 3 characters are capital letters, "
                    "the last 5 characters are numbers."
                )
            )
        ]
    )

    class Meta:
        model = Driver
        fields = ["license_number"]


class DriverLicenseUpdateForm(DriverLicenseForm):
    class Meta(DriverLicenseForm.Meta):
        fields = ["license_number"]


class DriverCreateForm(DriverLicenseForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta(DriverLicenseForm.Meta):
        fields = [
            "username",
            "first_name",
            "last_name",
            "license_number",
            "password"
        ]

    def save(self, commit=True):
        driver = super().save(commit=False)
        driver.set_password(self.cleaned_data["password"])
        if commit:
            driver.save()
        return driver


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
