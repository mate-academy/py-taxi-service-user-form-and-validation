from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from re import match

from taxi.models import Driver, Car


class LicenseValidationMixin:
    def clean_license_number(self) -> ValidationError | str:
        license_number = self.cleaned_data["license_number"]
        pattern = r"^[A-Z]{3}\d{5}$"
        if not match(pattern, license_number):
            raise ValidationError(
                "Driver license must consist only of 8 characters, "
                "first 3 characters are uppercase letters, "
                "last 5 characters are digits."
            )
        return license_number


class DriverCreationForm(UserCreationForm, LicenseValidationMixin):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self) -> ValidationError | str:
        return super().clean_license_number()


class DriverLicenseUpdateForm(forms.ModelForm, LicenseValidationMixin):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> ValidationError | str:
        return super().clean_license_number()


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
