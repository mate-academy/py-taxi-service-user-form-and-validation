from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from taxi.models import Car

User = get_user_model()


def validate_license(value):
    if len(value) != 8:
        raise ValidationError("License must be exactly 8 characters")
    if not value[:3].isalpha() or not value[:3].isupper():
        raise ValidationError("First 3 characters must be uppercase letters")
    if not value[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits")


class DriverCreationForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[validate_license],
        max_length=8
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "license_number")


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[validate_license],
        max_length=8
    )

    class Meta:
        model = User
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple
        }
