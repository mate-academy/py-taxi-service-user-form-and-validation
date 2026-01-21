from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicense:
    LICENSE_NUMBER_LENGTH = 8
    START_UPPERCASE_LENGTH = 3
    END_DIGITS_LENGTH = 5


def validate_license_number(license_number: str) -> str:
    if len(license_number) != DriverLicense.LICENSE_NUMBER_LENGTH:
        raise ValidationError(
            f"The length of the license number "
            f"must be {DriverLicense.LICENSE_NUMBER_LENGTH}"
        )
    if (
        not license_number[:DriverLicense.START_UPPERCASE_LENGTH].isalpha()
        or not license_number[:DriverLicense.START_UPPERCASE_LENGTH].isupper()
    ):
        raise ValidationError(
            f"The first {DriverLicense.START_UPPERCASE_LENGTH} "
            f"characters must be UPPERCASE LETTERS"
        )
    if not license_number[-DriverLicense.END_DIGITS_LENGTH:].isdigit():
        raise ValidationError(
            f"The last {DriverLicense.END_DIGITS_LENGTH} "
            f"characters must be NUMBERS"
        )
    return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )
