import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError

from .models import Car, Manufacturer, Driver
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field


def validate_license_number(license_number):
    if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
        raise ValidationError(
            "License must consist of 3 uppercase letters followed by 5 digits."
        )
    return license_number


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("name"),
            Field("country"),
            Submit("submit", "Save")
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("model"),
            Field("manufacturer"),
            Field("drivers"),
            Submit("submit", "Save")
        )


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number]
    )
    first_name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number")
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("username"),
            Field("first_name"),
            Field("last_name"),
            Field("license_number"),
            "password",
            "password2",
            Submit("submit", "Create")
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number]
    )

    class Meta:
        model = Driver
        fields = ["license_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("license_number"),
            Submit("submit", "Update License")
        )
