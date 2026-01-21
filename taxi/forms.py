from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(license_number) -> None:
    if not license_number or len(license_number) != 8:
        raise ValidationError(
            "The length of the license number must be 8 characters."
        )
    if not (license_number[:3].isupper() and license_number[:3].isalpha()):
        raise ValidationError("The first 3 characters must be uppercase.")
    if not license_number[3:].isdigit():
        raise ValidationError("The last 5 characters must be digits.")


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name"
        )

    def clean_license_number(self) -> object:
        license_number = self.cleaned_data.get("license_number")
        validate_license_number(license_number)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self) -> object:
        license_number = self.cleaned_data.get("license_number")
        validate_license_number(license_number)
        return license_number


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"

    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
