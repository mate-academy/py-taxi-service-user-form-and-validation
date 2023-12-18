from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class LicenseNumberValidationMixin:
    MIN_CHAR_CONSIST = 8

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.MIN_CHAR_CONSIST:
            raise ValidationError(
                f"Licence must consist only of "
                f"{self.MIN_CHAR_CONSIST} characters"
            )

        if not license_number[:3].isalpha():
            raise ValidationError(
                "First 3 characters must be uppercase letters."
            )

        if not license_number[-5:].isdigit():
            raise ValidationError("Last 5 characters must be digits.")

        return license_number


class DriverCreationForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
