from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )


class DriverLicenseUpdateForm(forms.ModelForm):
    LENGTH_LICENSE = 8

    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        start_length = license_number[:3]

        if len(license_number) != DriverLicenseUpdateForm.LENGTH_LICENSE:
            raise ValidationError(
                "Length license number must be"
                f" {DriverLicenseUpdateForm.LENGTH_LICENSE}"
            )

        if (
                not start_length.isalpha()
                or start_length != start_length.upper()
        ):
            raise ValidationError(
                "First 3 characters have to be uppercase letters"
            )
        if not license_number[3:].isdigit():
            raise ValidationError(
                "Last 5 characters have to be digits"
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
