from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from .models import Driver, Car


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}\d{5}$",
                message="License number must consist of 8 characters: "
                        "first 3 uppercase letters and last 5 digits.",
            )
        ],
        help_text="Format: AAA12345"
    )

    class Meta:
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number")


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}\d{5}$",
                message="License number must consist of 8 characters: "
                        "first 3 uppercase letters and last 5 digits.",
            )
        ],
        help_text="Format: AAA12345"
    )

    class Meta:
        model = Driver
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ["manufacturer", "model", "drivers"]
