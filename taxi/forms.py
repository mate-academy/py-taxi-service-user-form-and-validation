from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Car


def validate_license(license_number: str):
    length = (len(license_number) == 8)
    letters = all(
        char.isalpha() and char.isupper() for char in license_number[:3]
    )
    digits = all(char.isnumeric() for char in license_number[3:])
    if not all((length, letters, digits),):
        raise ValidationError(
            "License number requirements: consist only of 8 characters, "
            "first 3 characters are UPPERCASE letters, "
            "last 5 characters are digits."
        )


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(validators=[validate_license])

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(validators=[validate_license])

    class Meta:
        model = get_user_model()
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
