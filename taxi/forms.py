from django import forms
from django.contrib.auth.forms import UserCreationForm
<<<<<<< HEAD
from django.core.exceptions import ValidationError

from .models import Car, Driver
=======
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

from .models import Car

User = get_user_model()
>>>>>>> e5c2855716448c357c0e3c42aeac3e8e33b1fc07


class LicenseValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
<<<<<<< HEAD

        if len(license_number) != 8:
            raise ValidationError(
                "License number must be exactly 8 characters."
            )

        if (
            not license_number[:3].isalpha()
            or not license_number[:3].isupper()
        ):
            raise ValidationError(
                "First 3 characters must be uppercase letters."
            )

        if not license_number[-5:].isdigit():
            raise ValidationError(
                "Last 5 characters must be digits."
            )

        return license_number


class DriverCreationForm(
    LicenseValidationMixin,
    UserCreationForm
):
    class Meta:
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(
    LicenseValidationMixin,
    forms.ModelForm
):
    class Meta:
        model = Driver
=======
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise ValidationError(
                "License number must consist of 8 characters: "
                "first 3 uppercase letters followed by 5 digits."
            )
        return license_number


class DriverCreationForm(LicenseValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "license_number")


class DriverLicenseUpdateForm(LicenseValidationMixin, forms.ModelForm):
    class Meta:
        model = User
>>>>>>> e5c2855716448c357c0e3c42aeac3e8e33b1fc07
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
<<<<<<< HEAD
        fields = ("model", "manufacturer", "drivers")
=======
        fields = "__all__"
>>>>>>> e5c2855716448c357c0e3c42aeac3e8e33b1fc07
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
