from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Driver, Car
import re


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = ["username", "first_name", "last_name",
                  "license_number", "password1", "password2"]


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.fullmatch(r"[A-Z]{3}\d{5}", license_number):
            raise ValidationError(
                "License must consist of 8 characters: first 3 are uppercase "
                "letters, last 5 are digits."
            )
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
