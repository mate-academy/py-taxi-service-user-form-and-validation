from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import (
    Driver,
    Car
)


def validate_license_number(value: str):
    if len(value) != 8:
        raise ValidationError(
            "Invalid license number. "
            "Length of license number must be 8 characters."
        )
    if not value[:3].isalpha():
        raise ValidationError(
            "Invalid license number. "
            "First three characters be letters."
        )
    if value[:3] != value[:3].upper():
        raise ValidationError(
            "Invalid license number. "
            "First 3 characters must be uppercase letters."
        )
    if not value[3:].isdigit():
        raise ValidationError(
            "Invalid license number. "
            "Last 5 characters must be digits."
        )
    return value


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class DriverForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[
            validate_license_number
        ]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "username",
            "email",
            "first_name",
            "last_name",
            "license_number"
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
