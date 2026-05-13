import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car


LICENSE_NUMBER_PATTERN = re.compile(r"^[A-Z]{3}\d{5}$")


def validate_license_number(license_number):
    if not LICENSE_NUMBER_PATTERN.match(license_number):
        raise forms.ValidationError(
            "License number must contain exactly 8 characters: "
            "first 3 uppercase letters and last 5 digits."
        )
    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
