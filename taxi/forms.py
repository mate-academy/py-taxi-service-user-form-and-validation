from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class LicenseValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if not license_number:
            return license_number

        if len(license_number) != 8:
            raise ValidationError("License number must be 8 characters long.")

        if (
            not license_number[:3].isupper()
            or not license_number[:3].isalpha()
        ):
            raise ValidationError(
                "Invalid license number:"
                " The first three characters must be uppercase letters"
            )

        if not license_number[3:].isdigit():
            raise ValidationError(
                "Invalid license number: The last 5 characters must be numbers"
            )

        return license_number


class DriverCreationForm(LicenseValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )


class DriverLicenseUpdateForm(LicenseValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
