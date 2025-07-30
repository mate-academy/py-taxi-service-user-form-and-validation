import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.views import generic

from taxi.models import Driver, Car


class DriverCreationForm (UserCreationForm):
    class Meta :
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not re.fullmatch(r"[A-Z]{3}\d{5}", license_number):
            raise ValidationError(
                "License number must be 3 uppercase letters followed by 5 digits (e.g., ABC12345)"
            )
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta :
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(
                "Ensure that length of license_number is 8"
            )

        if not license_number[:2].isupper():
            raise ValidationError(
                "Ensure that first 3 letters of license_number is uppercase"
            )

        if not license_number[3:].isdigit():
            raise ValidationError(
                "Ensure that last 5 characters is numbers"
            )
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta :
        model = Car
        fields = "__all__"
