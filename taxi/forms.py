from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(license_number):

    if len(license_number) != 8:

        raise ValidationError(
            "The driver's license must be 8 characters long."
        )

    first_part = license_number[:3]

    if not first_part.isupper() or not first_part.isalpha():

        raise ValidationError(
            "The first 3 characters must be uppercase letters"
        )

    if not license_number[3:].isdecimal():

        raise ValidationError("The last 5 characters must be digits")


class DriverCreateForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        ) + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
