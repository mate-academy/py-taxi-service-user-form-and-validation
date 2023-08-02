from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[
            RegexValidator(
                r"^[A-Z]{3}[0-9]{5}$",
                "License number must have:"
                "total 8 chars: first 3 upper letters, last 5 digits"
            ),
        ]
    )

    class Meta:
        model = Driver
        fields = ["license_number"]


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[
            RegexValidator(
                r"^[A-Z]{3}[0-9]{5}$",
                "License number must have:"
                "total 8 chars: first 3 upper letters, last 5 digits"
            )
        ]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverUpdateCarsForm(forms.HiddenInput):
    class Meta:
        model = Driver
        fields = ("",)
