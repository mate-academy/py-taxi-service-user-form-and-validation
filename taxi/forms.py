from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
from taxi.models import Driver, Car


class LicenseNumberValidatorMixin:
    @staticmethod
    def validate(license_number) -> str | ValidationError:
        if (
            (len(license_number) != 8)
            or (license_number[:3] != license_number[:3].upper())
            or (not (license_number[:3]).isalpha())
            or (not license_number[3:].isnumeric())
        ):
            raise ValidationError(
                "License number must be 8 characters long, "
                "start with 3 uppercase letters, and end with 5 numbers"
            )

        return license_number


class DriverCreationForm(UserCreationForm, LicenseNumberValidatorMixin):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number",
        )

    def clean_license_number(self) -> str:
        return self.validate(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm, LicenseNumberValidatorMixin):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str | ValidationError:
        return self.validate(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
