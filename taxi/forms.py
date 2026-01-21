from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(license_number: str) -> None:
    if not len(license_number) == 8:
        raise ValidationError(
            f"License number must consist of 8 characters,"
            f"{len(license_number)} given."
        )
    if (
        not license_number[:3].isalpha()
        or license_number[:3] != license_number[:3].upper()
    ):
        raise ValidationError("First 3 characters must be uppercase letters.")
    if not license_number[3:].isnumeric():
        raise ValidationError("Last 5 characters must be digits.")


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=16, validators=[validate_license_number]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=16, validators=[validate_license_number]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
