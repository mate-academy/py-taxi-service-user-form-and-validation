from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreatForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )
        help_texts = {
            "license_number":
                "License number should consist of 8 characters. "
                "The first 3 characters should be uppercase letters, "
                "and the last 5 characters should be digits. "
                "For example 'JON26231'"
        }

    def clean_license_number(self):
        return license_validator(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]
        help_texts = {
            "license_number":
                "License number should consist of 8 characters. "
                "The first 3 characters should be uppercase letters, "
                "and the last 5 characters should be digits. "
                "For example 'JON26231'"
        }

    def clean_license_number(self):
        return license_validator(self.cleaned_data["license_number"])


def license_validator(
        license_number
):
    if len(license_number) != 8:
        raise ValidationError("License number should be 8 characters")
    elif not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError(
            "First 3 characters should be uppercase and letters"
        )
    elif not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters should be digits")

    return license_number
