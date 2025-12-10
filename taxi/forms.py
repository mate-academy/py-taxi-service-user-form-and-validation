from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from taxi.models import Car


def validate_license_number(value):
    if len(value) != 8:
        raise ValidationError(
            "License number must be exactly 8 characters: "
            "first 3 uppercase letters (A-Z), then 5 digits (0-9)."
        )

    if not value[:3].isalpha() or not value[:3].isupper():
        raise ValidationError("First 3 characters must be uppercase letters")

    if not value[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits")


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "license_number",
        ]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
