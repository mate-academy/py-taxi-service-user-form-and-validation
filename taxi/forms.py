from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator,
)

from .models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    MIN_LICENSE_LENGTH = 8
    MAX_LICENSE_LENGTH = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    license_number = forms.CharField(
        required=True,
        validators=[
            MinLengthValidator(
                MIN_LICENSE_LENGTH,
                message=f"Minimum length {MIN_LICENSE_LENGTH}"
            ),
            MaxLengthValidator(
                MAX_LICENSE_LENGTH,
                message=f"Maximum length {MAX_LICENSE_LENGTH}"
            ),
            RegexValidator(
                regex=r"[A-Z]{3}[0-9]{5}",
                message="First 3 characters are uppercase letters, "
                        "last 5 characters are digits")
        ]
    )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
