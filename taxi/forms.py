import re

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = str(
            self.cleaned_data.get("license_number", "")
        )

        pattern = r"^[A-Z]{3}[0-9]{5}$"

        if not re.fullmatch(pattern, license_number):
            raise forms.ValidationError(
                "License must consist of 3 uppercase letters and 5 digits"
            )

        return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = str(
            self.cleaned_data.get("license_number", "")
        )

        pattern = r"^[A-Z]{3}[0-9]{5}$"

        if not re.fullmatch(pattern, license_number):
            raise forms.ValidationError(
                "License must consist of 3 uppercase letters and 5 digits"
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
