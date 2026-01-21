from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import models

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(models.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "Driver license consist of 8 characters"
            )
        if (
                not (license_number[:3].isalpha()
                     and license_number[:3].isupper())
        ):
            raise ValidationError(
                "Driver license should starts with 3 capital letters"
            )
        if not license_number[-5:].isdigit():
            raise ValidationError(
                "Last 5 characters in license number should be digit"
            )
        return license_number


class DriverCreateForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if (
                len(license_number) != 8
                or not (license_number[:3].isalpha()
                        and license_number[:3].isupper())
                or not license_number[-5:].isdigit()
        ):
            raise ValidationError("License must consist 8 characters "
                                  "and start from 3 capital letters "
                                  "and 5 last characters should be digital"
                                  )
        return license_number


class CarForm(models.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
