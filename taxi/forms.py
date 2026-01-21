from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


def validation_license_number(license_number):
    correct_license_number_len = 8

    if len(license_number) != correct_license_number_len:
        raise ValidationError(
            f"License number must be "
            f"{correct_license_number_len} characters long."
        )
    elif not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError("First 3 characters must be uppercase letters.")
    elif not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits.")

    return license_number


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(validators=[validation_license_number])

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number", "email", "first_name", "last_name"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(validators=[validation_license_number])

    class Meta:
        model = Driver
        fields = ("license_number",)
