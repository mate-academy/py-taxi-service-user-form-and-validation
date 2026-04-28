from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
import re

from taxi.models import Driver, Car


def clean_license_number(license_number):
    if not re.fullmatch(r"[A-Z]{3}\d{5}", license_number):
        raise ValidationError(
            "License number must start with 3 uppercase letters "
            "followed by 5 digits"
        )

    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    license_number = forms.CharField(validators=[clean_license_number])


class DriverUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("first_name", "last_name", "license_number",)

    def clean_license_number(self):
        return clean_license_number(self.cleaned_data.get("license_number"))


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        return clean_license_number(self.cleaned_data.get("license_number"))


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
