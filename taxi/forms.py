from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField

from taxi.models import Driver, Car


def license_number_validator() -> CharField:
    license_validator = RegexValidator(
        regex=r"^[A-Z]{3}\d{5}$",
        message="Driver's license must be 8 characters long: "
        "3 uppercase letters followed by 5 digits.",
    )
    license_number = forms.CharField(
        max_length=8,
        validators=[
            license_validator,
        ],
        help_text="Enter your driver's license (e.g., ABC12345)",
    )
    return license_number


class DriverCreationForm(UserCreationForm):
    license_number = license_number_validator()

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
            "email",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = license_number_validator()

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Car
        fields = "__all__"
