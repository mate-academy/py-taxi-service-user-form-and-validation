from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Driver, Car


def validate_len(value: str) -> None:
    correct_len = 8

    if len(value) != correct_len:
        raise ValidationError(
            f"Ensure that length of value is {correct_len}"
        )


def validate_characters(value: str) -> None:
    num_of_letters = 3
    num_of_digits = 5

    if not (value[:num_of_letters].isalpha()
            and value[:num_of_letters].isupper()):
        raise ValidationError(
            f"Ensure that first {num_of_letters} characters "
            "are uppercase letters"
        )
    if not value[num_of_letters:].isdigit():
        raise ValidationError(
            f"Ensure that last {num_of_digits} characters are digits"
        )


class DriverLicenseUpdateForm(forms.ModelForm):

    license_number = forms.CharField(
        required=True,
        validators=[
            validate_len,
            validate_characters
        ]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
