from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    LENGTH_LICENSE_NUMBER = 8

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number"
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if (len(license_number)
                != DriverLicenseUpdateForm.LENGTH_LICENSE_NUMBER):
            raise ValidationError(
                f"Ensure that length license_number is "
                f"{DriverLicenseUpdateForm.LENGTH_LICENSE_NUMBER}"
            )

        if license_number[:3].isdigit() or license_number[:3].islower():
            raise ValidationError("Ensure that first 3 letters "
                                  "in license_number are in uppercase")

        if not license_number[3:].isdigit():
            raise ValidationError("Ensure that after 3 letters "
                                  "in license_number are only digits")
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
