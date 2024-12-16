import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, get_user_model
from django.core.exceptions import ValidationError

from .models import Car


class DriverCreationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    license_number = forms.CharField()

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "username",
            "email", "password1", "password2",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_NUMBER_LENGTH = 8

    class Meta:
        model = get_user_model()
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if get_user_model().objects.filter(
                license_number=license_number
        ).exists():
            raise ValidationError(
                "A driver with this license"
                " number already exists."
            )

        if len(license_number) != self.LICENSE_NUMBER_LENGTH:
            raise forms.ValidationError(
                f"License number must consist of "
                f"{self.LICENSE_NUMBER_LENGTH} characters."
            )
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise forms.ValidationError(
                "License number must start with 3 uppercase"
                " letters followed by 5 digits."
            )

        return license_number


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
        widgets = {
            "drivers": forms.CheckboxSelectMultiple()
        }
