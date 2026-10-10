from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from django import forms

from taxi.models import Driver, Car


class LicenseValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise ValidationError(
                "Ensure that license number is 8 characters long"
            )
        if (license_number[:3] != license_number[:3].upper()
                or not license_number[:3].isalpha()):
            raise ValidationError(
                "Ensure that 3 first elements are uppercase letters"
            )
        if not license_number[3:].isdigit():
            raise ValidationError("Ensure that 5 last elements are numbers")
        return license_number


class DriverLicenseUpdateForm(LicenseValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]


class DriverCreationForm(LicenseValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number"
        )


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
