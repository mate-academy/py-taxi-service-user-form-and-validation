from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


def validate_driver_license(license_number: str) -> None:
    if not (
            len(license_number) == 8
            and license_number[:3].isalpha()
            and license_number[:3].isupper()
            and license_number[3:].isdigit()
    ):
        raise ValidationError(
            "The license must satisfy following conditions: "
            "1) consist only of 8 characters; "
            "2) first 3 characters are uppercase letters; "
            "3) last 5 characters are digits."
        )


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=63,
        validators=[validate_driver_license],
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=63,
        validators=[validate_driver_license],
    )

    class Meta:
        model = Driver
        fields = ("license_number",)
