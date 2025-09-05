from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver
from django import forms


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError("License must be 8 characters long.")
    if not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError("First 3 characters must be uppercase letters.")
    if not license_number[3:].isdigit():
        raise ValidationError("First 5 characters must be digits.")


class DriverCreateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("username", "first_name", "last_name",
                  "email", "password", "license_number")

    license_number = forms.CharField(validators=[validate_license_number])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)
    license_number = forms.CharField(validators=[validate_license_number])


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
