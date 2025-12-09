from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number",
        )

    def clean_license_number(self) -> str:
        return license_number_validation(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        return license_number_validation(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


def license_number_validation(license_number: str) -> str:
    if len(license_number) != 8:
        raise ValidationError(
            "Ensure that license number consist of 8 characters!"
        )

    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError(
            "First three symbols of license number must be uppercase letters."
        )

    if not license_number[3:].isdigit():
        raise ValidationError(
            "Last five symbols of license number must be digits."
        )

    return license_number
