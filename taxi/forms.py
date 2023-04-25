from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


def validate_license(license_number) -> str:
    if len(license_number) != 8:
        raise ValidationError(
            "License number must be 8 symbols"
        )

    elif (
        not license_number[:3].isalpha()
        or not license_number[:3].isupper()
    ):
        raise ValidationError(
            "The license number must start with three capital letters"
        )

    elif not license_number[3:].isnumeric():
        raise ValidationError(
            "The license number must end with five digits"
        )
    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
            "email"
        )

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        license_number = validate_license(license_number)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        license_number = validate_license(license_number)
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class ChangeDriverForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = []
