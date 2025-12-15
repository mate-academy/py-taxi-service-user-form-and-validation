from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class LicenseNumberValidationMixin:
    LICENSE_LENGTH = 8

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if not license_number:
            return license_number

        if len(license_number) != self.LICENSE_LENGTH:
            raise ValidationError(
                f"Ensure that count of char is {self.LICENSE_LENGTH}"
            )

        if (
                not license_number[:3].isalpha()
                or not license_number[:3].isupper()
        ):
            raise ValidationError(
                "First 3 symbols should be uppercase letters"
            )

        if not license_number[3:].isdigit():
            raise ValidationError(
                "Last 5 symbols should be digits"
            )

        return license_number


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["license_number"]


class DriverForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "first_name",
            "last_name",
            "password",
            "license_number",
        ]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
