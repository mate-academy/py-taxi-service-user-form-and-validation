from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)

from .models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    MESSAGE = "License number should consist of"\
              " 3 uppercase letters and 5 digits"
    REGEX = "[A-Z]{3}[0-9]{5}"

    license_number = forms.CharField(
        required=True,
        validators=[
            MaxLengthValidator(8),
            MinLengthValidator(8),
            RegexValidator(REGEX, MESSAGE)
        ]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverCreateForm(UserCreationForm, DriverLicenseUpdateForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "license_number",
        )


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
