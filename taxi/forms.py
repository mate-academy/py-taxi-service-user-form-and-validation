from __future__ import annotations
from string import ascii_uppercase

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverForm(UserCreationForm):
    license_number = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data.get("license_number"))


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data.get("license_number"))


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"


def validate_license_number(license_number):
    if (
            len(license_number) != 8
            or not license_number[:3].isupper()
            or not license_number[:3].isalpha()
            or not license_number[3:].isdigit()
    ):
        raise forms.ValidationError("Provide proper license number")
    return license_number
