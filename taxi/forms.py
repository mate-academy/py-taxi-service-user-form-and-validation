from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def clean_license_number(license_number):

    if len(license_number) != 8:
        raise ValidationError("License number must be 8 characters long")

    for character in license_number[:3]:
        if character != character.upper() or character.isdigit():
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )
    for character in license_number[3:]:
        if not character.isdigit():
            raise ValidationError("Last 5 characters must be digits")

    return license_number


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        validators=[clean_license_number]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "email", "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[clean_license_number]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
