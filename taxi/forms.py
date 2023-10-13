from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from taxi.models import Car


def clean_license_number(license_number: str) -> str:
    if len(license_number) != 8:
        raise forms.ValidationError(
            "License number must be exactly 8 characters long."
        )
    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise forms.ValidationError(
            "The first 3 characters must be uppercase letters."
        )
    if not license_number[-5:].isdigit():
        raise forms.ValidationError("The last 5 characters must be digits.")
    return license_number


class LicenseNumberField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(clean_license_number)
        self.help_text = (
            "Enter a valid 8-character license number (e.g., ABC12345)."
        )


class DriverCreationForm(UserCreationForm):
    license_number = LicenseNumberField()

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = LicenseNumberField()

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
