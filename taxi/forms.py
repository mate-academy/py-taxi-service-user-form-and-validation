from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return driver_license_validator(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    form_fields = ["license_number"]

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return driver_license_validator(license_number)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


def driver_license_validator(value: str) -> str | ValidationError:
    if len(value) != 8:
        raise ValidationError(
            "Invalid license number (Consist only of 8 characters)"
        )

    if (not value[:3].isupper()
            or not value[:3].isalpha()):
        raise ValidationError(
            "First 3 characters must be are uppercase letters"
        )

    if not value[3:].isdigit():
        raise ValidationError("Last 5 characters must be are digits")

    return value
