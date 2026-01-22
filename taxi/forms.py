from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car

LICENSE_NUMBER_LENGTH = 8
FIRST_CHAR_LENGTH = 3
LAST_CHAR_LENGTH = 5


def clean_license(license_number: str) -> None:
    if len(license_number) != LICENSE_NUMBER_LENGTH:
        raise ValidationError(
            f"License has to be {LICENSE_NUMBER_LENGTH} characters long"
        )
    if not (license_number[:FIRST_CHAR_LENGTH].isupper()
            and license_number[:FIRST_CHAR_LENGTH].isalpha()):
        raise ValidationError(
            f"First {FIRST_CHAR_LENGTH} characters must be uppercase"
        )
    if not license_number[-LAST_CHAR_LENGTH:].isdigit():
        raise ValidationError(
            f"Last {LAST_CHAR_LENGTH} characters must be digits"
        )


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        clean_license(license_number)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        clean_license(license_number)
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
