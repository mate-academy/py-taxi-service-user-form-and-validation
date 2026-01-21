from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import (
    ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
)

from taxi.models import Car, Driver


class CarCreateForm(ModelForm):
    drivers = ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class DriverLicenseUpdateForm(ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


def validate_license_number(value: str) -> str:
    if len(value) != 8:
        raise ValidationError("License must consist only of 8 characters")
    elif not value[:3].isalpha() or not value[:3].isupper():
        raise ValidationError(
            "First 3 characters of license are not uppercase or letters"
        )
    elif not value[3:].isdigit():
        raise ValidationError("Last 5 characters are not digits")
    return value
