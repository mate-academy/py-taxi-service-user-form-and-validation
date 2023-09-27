from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError
from django.forms import TextInput

from taxi.models import Driver, Car

LICENSE_LENGTH = 8


class CarForm(forms.ModelForm):
    drivers = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("username", "password", "license_number")
        labels = {"username": "Username", "password": "Password"}
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "enter your username",
                    "autocomplete": "off"
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "placeholder": "********",
                    "autocomplete": "off",
                    "data-toggle": "password",
                }
            ),
            "license_number": forms.TextInput(
                attrs={"placeholder": "XXX00000", "autocomplete": "on"}
            ),
        }


class DriverLicenseUpdateForm(forms.ModelForm):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != LICENSE_LENGTH:
            raise ValidationError(
                f"Ensure, that your license number consist "
                f"{LICENSE_LENGTH} characters!"
            )

        if not license_number[:3].isalpha():
            raise ValidationError(
                "Ensure, that your first 3 characters are letters!"
            )

        if license_number[:3] != license_number[:3].upper():
            raise ValidationError(
                "Ensure, that your first 3 characters "
                "are uppercase characters!"
            )

        if not license_number[3:].isdigit():
            raise ValidationError(
                "Ensure, that your license number " "consist of 5 numbers!"
            )
        return license_number

    class Meta:
        model = Driver
        fields = ("license_number",)
