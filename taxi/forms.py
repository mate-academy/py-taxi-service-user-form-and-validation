from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class CustomUser:
    pass


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "username",
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if license_number:
            validate_license_number(license_number)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if license_number:
            validate_license_number(license_number)
        return license_number


class DriverLicenseDeleteForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = []

    def save(self, commit=True):
        driver = super().save(commit=False)
        driver.license_number = ""
        if commit:
            driver.save()
        return driver


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


def validate_license_number(value):
    if len(value) != 8:
        raise ValidationError("License number must be 8 characters long.")
    if not (
            value[:3].isalpha() and value[:3].isupper() and value[3:].isdigit()
    ):
        raise ValidationError(
            "License number must consist of 3 uppercase letters followed by 5 "
            "digits."
        )
