from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class LicenseNumberValidationMixin:
    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        current_driver = self.instance
        if len(license_number) != 8:
            raise ValidationError(
                "License number must be exactly 8 digits long."
            )

        license_code, license_digits = license_number[:3], license_number[3:]
        if not license_digits.isdigit():
            raise ValidationError(
                "The last 5 characters must be digits"
            )

        if not (license_code.isupper() and license_code.isalpha()):
            raise ValidationError(
                "The first 3 characters must be uppercase letters."
            )

        if Driver.objects.exclude(pk=current_driver.pk
                                  ).filter(license_number=license_number
                                           ).exists():
            raise ValidationError("License number already exists.")

        return license_number


class DriverCreationForm(UserCreationForm, LicenseNumberValidationMixin):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name"
        )


class DriverLicenseUpdateForm(forms.ModelForm, LicenseNumberValidationMixin):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
