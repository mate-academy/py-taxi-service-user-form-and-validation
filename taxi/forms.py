from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import (
    ModelForm,
    ModelMultipleChoiceField,
    CheckboxSelectMultiple,
)

from .models import Driver, Car


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError("License number must contain 8 characters")
    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError("First 3 characters must be uppercase letters")
    if not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters must be numeric")


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class DriverLicenseUpdateForm(ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class CarCreateForm(ModelForm):
    drivers = ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
