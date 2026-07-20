from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Car


class LicenseValidationMixin:

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(
                "The length of the license number "
                f"must be 8 characters, not {len(license_number)}."
            )

        if license_number[:3] != license_number[:3].upper():
            raise ValidationError(
                "The first 3 characters must be capital letters."
            )

        if not all([char.isalpha() for char in license_number[:3]]):
            raise ValidationError(
                "The first 3 characters must "
                "contain only uppercase letters."
            )

        if not all([char.isdigit() for char in license_number[3:]]):
            raise ValidationError(
                "The last 5 characters must be numbers."
            )

        return license_number


class DriverCreationForm(LicenseValidationMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )


class DriverLicenseUpdateForm(LicenseValidationMixin, UserChangeForm):

    password = None

    class Meta:
        model = get_user_model()
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
