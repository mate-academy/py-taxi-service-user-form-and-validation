from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver

LICENSE_NUMBER_LENGTH = 8
LICENSE_LETTERS = 3


def validate_license_number(license_number: str) -> str:
    if len(license_number) != LICENSE_NUMBER_LENGTH:
        raise ValidationError(
            f"License number should consist of "
            f"{LICENSE_NUMBER_LENGTH} characters"
        )
    letters = license_number[:LICENSE_LETTERS]
    digits = license_number[LICENSE_LETTERS:]
    if not (letters.isascii() and letters.isalpha() and letters.isupper()):
        raise ValidationError(
            f"First {LICENSE_LETTERS} characters should be uppercase letters"
        )
    if not (digits.isascii() and digits.isdigit()):
        raise ValidationError(
            f"Last {LICENSE_NUMBER_LENGTH - LICENSE_LETTERS} characters "
            f"should be digits"
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

    def clean_license_number(self) -> str:
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        return validate_license_number(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
