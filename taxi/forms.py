from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError("License number must be 8 characters long.")
    if (not license_number[:3].isalpha()
            or not license_number[:3].isupper()):
        raise ValidationError(
            "First 3 characters must be uppercase letters."
        )
    if not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits.")


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[validate_license_number, ]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name",
                                                 "last_name",
                                                 "license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[validate_license_number, ]
    )

    class Meta:
        model = Driver
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
