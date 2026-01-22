from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator
)

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    MESSAGE = "License number should consist of" \
              " first 3 uppercase letters and after 5 digits"
    REGEX = "[A-Z]{3}[0-9]{5}"
    LEN_OF_LICENSE_NUMBER = 8
    license_number = forms.CharField(
        required=True,
        validators=[
            MaxLengthValidator(LEN_OF_LICENSE_NUMBER),
            MinLengthValidator(LEN_OF_LICENSE_NUMBER),
            RegexValidator(REGEX, MESSAGE)
        ]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverCreationForm(UserCreationForm):
    MESSAGE = "License number should consist of" \
              " first 3 uppercase letters and after 5 digits"
    REGEX = "[A-Z]{3}[0-9]{5}"
    LEN_OF_LICENSE_NUMBER = 8
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    license_number = forms.CharField(
        required=True,
        validators=[
            MaxLengthValidator(LEN_OF_LICENSE_NUMBER),
            MinLengthValidator(LEN_OF_LICENSE_NUMBER),
            RegexValidator(REGEX, MESSAGE)
        ]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
            "email",
        )


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
