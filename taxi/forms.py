from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from taxi.models import Car
import re

User = get_user_model()


def validate_license_number(value):
    pattern = r"^[A-Z]{3}\d{5}$"
    if not re.match(pattern, value):
        raise ValidationError(
            "License number must contain 3 uppercase letters and 5 digits"
        )


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(validators=[validate_license_number])

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(validators=[validate_license_number])

    class Meta:
        model = User
        fields = ("license_number",)


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
