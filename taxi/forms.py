from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = "__all__"

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


def validate_license_number(license_number: str) -> str:

    if len(license_number) != 8:
        raise ValidationError("length must be 8 symbols")
    if (
            not license_number[:3].isalpha()
            or license_number[:3] != license_number[:3].upper()
    ):
        raise ValidationError("first 3 symbols must be in uppercase")
    if not license_number[-5:].isdigit():
        raise ValidationError("last 5 symbols must be digit")

    return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
