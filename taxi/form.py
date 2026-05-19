from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


def validate_license_number(license_number: str) -> str:
    """
    Validate that license number:
    - Consists of exactly 8 characters
    - First 3 characters are uppercase letters
    - Last 5 characters are digits
    """
    if len(license_number) != 8:
        raise forms.ValidationError(
            "License number must consist of exactly 8 characters."
        )
    if not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise forms.ValidationError(
            "First 3 characters of license number must be uppercase letters."
        )
    if not license_number[3:].isdigit():
        raise forms.ValidationError(
            "Last 5 characters of license number must be digits."
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
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
