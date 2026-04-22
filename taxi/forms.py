from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from taxi.models import Driver, Car


def validate_license_number(value: str) -> None:
    if len(value) != 8:
        raise ValidationError("License number should consist of 8 characters")

    if not (value[:3].isalpha() and value[:3].isupper()):
        raise ValidationError("First 3 characters should be uppercase letters")

    if not value[3:].isdigit():
        raise ValidationError("Last 5 characters should be digits")


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
