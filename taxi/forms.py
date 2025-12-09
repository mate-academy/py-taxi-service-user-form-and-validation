from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver


class DriverUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Driver
        fields = "__all__"


def validate_license_number(license_number: str) -> str:
    licence_correct_len = 8

    license_len = len(license_number)
    license_start = license_number[:3]
    license_end = license_number[3:]

    if license_len != licence_correct_len:
        raise ValidationError(
            f"License number len should be {licence_correct_len} characters."
        )
    if not license_start.isupper() or not license_start.isalpha():
        raise ValidationError(
            "License number should starts with 3 upper case letters."
        )
    if not license_end.isdigit():
        raise ValidationError(
            "License number should end with 5 digits."
        )
    return license_number
