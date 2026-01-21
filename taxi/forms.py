from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxLengthValidator, RegexValidator
from django.forms import ModelForm
from pyexpat.errors import messages

from taxi.models import Driver, Car
LIMITED_LENGTH = 8


class DriverCreateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[
            MaxLengthValidator(
                LIMITED_LENGTH,
                message="length of license number must be equal to 8"
            ),
            RegexValidator(
                regex=r"^[A-Z]{3}\d{5}$",
                message="license must contain 3 upper letters and 5 nums"
            ),

        ]
    )

    class Meta:
        model = Driver
        fields = (
            "username",
            "password",
            "email",
            "license_number",
        )


class DriverLicenseUpdateForm(DriverCreateForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Car
        fields = "__all__"
