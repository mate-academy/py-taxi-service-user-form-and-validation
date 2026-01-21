from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car

LICENCE_LENGTH = 8
FIRST_UPPER_LETTER_NUMBER = 3
LAST_DIGITS_NUMBER = LICENCE_LENGTH - FIRST_UPPER_LETTER_NUMBER


def validate_license_number(license_number: str) -> str:
    if len(license_number) != LICENCE_LENGTH:
        raise ValidationError(
            f"Licence must have exactly {LICENCE_LENGTH} characters"
        )
    if not (license_number[:FIRST_UPPER_LETTER_NUMBER].isupper()
            and license_number[:FIRST_UPPER_LETTER_NUMBER].isalpha()):
        raise ValidationError(
            f"First {FIRST_UPPER_LETTER_NUMBER} characters "
            f"must be uppercase letters"
        )
    if not license_number[FIRST_UPPER_LETTER_NUMBER:].isdigit():
        raise ValidationError(
            f"Last {LAST_DIGITS_NUMBER} characters must be digits"
        )
    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number", ]

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
