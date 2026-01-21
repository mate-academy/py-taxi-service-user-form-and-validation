from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    LEN_LICENSE = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not (len(license_number) == self.LEN_LICENSE):
            raise ValidationError(
                f"Length of driver license should be {self.LEN_LICENSE}"
            )
        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise ValidationError(
                "First 3 characters should be uppercase letters"
            )
        if not (license_number[3:].isdigit()):
            raise ValidationError("Last 5 characters should be digits")

        return license_number


class DriverCreationForm(UserCreationForm, DriverLicenseUpdateForm):

    class Meta:
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number")


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
