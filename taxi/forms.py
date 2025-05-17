from django.contrib.auth.forms import UserCreationForm
from django import forms
import re

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        data = self.cleaned_data["license_number"]
        if not re.match(r"^[A-Z]{3}\d{5}$", data):
            raise forms.ValidationError(
                "License must have 3 uppercase letters followed by 5 digits."
            )
        return data


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(max_length=8, min_length=8)

    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        data = self.cleaned_data["license_number"]
        if not re.match(r"^[A-Z]{3}\d{5}$", data):
            raise forms.ValidationError(
                "License must have 3 uppercase letters followed by 5 digits."
            )
        return data


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
