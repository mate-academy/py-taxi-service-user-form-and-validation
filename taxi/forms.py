from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


def validate_license_number(value: str) -> str:
    if len(value) != 8:
        raise ValidationError(
            "License number must be"
            " 8 characters long!"
            " Example: ABC12345"
        )
    if not value[:3].isalpha():
        raise ValidationError(
            "The first three characters"
            " must be letters!"
            " Example: ABC12345"
        )
    if value[:3] != value[:3].upper():
        raise ValidationError(
            "The first three letters"
            " must be capitalized!"
            " Example: ABC12345")
    if not value[3:].isdigit():
        raise ValidationError(
            "The last 5 characters"
            " must be numbers!"
            " Example: ABC12345")
    return value


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[validate_license_number]
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
        required=True,
        validators=[validate_license_number]
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
