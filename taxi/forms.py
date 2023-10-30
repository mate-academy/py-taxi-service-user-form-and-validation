from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from .models import Driver, Car


def create_license_pattern():
    license_number_pattern = r"^[A-Z]{3}\d{5}$"

    license_number_validator = RegexValidator(
        regex=license_number_pattern,
        message="Enter a valid license number.",
        code="invalid_license_number",
    )
    license_number = forms.CharField(
        validators=[license_number_validator],
        max_length=8,
        label="License Number"
    )

    return license_number


class DriverCreateForm(UserCreationForm):
    license_number = create_license_pattern()

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = create_license_pattern()

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
