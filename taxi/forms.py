from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_LEN = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != DriverLicenseUpdateForm.LICENSE_LEN:
            raise ValidationError(
                f"Ensure that license is =="
                f"{DriverLicenseUpdateForm.LICENSE_LEN} character long."
            )
        elif (license_number[:3] != license_number[:3].upper()
              or any(char.isdigit() for char in license_number[:3])):
            raise ValidationError(
                "Ensure that license number is correct"
            )
        elif not license_number[3:].isdigit():
            raise ValidationError("Invalid license number")
        return license_number


class DriverForm(UserCreationForm):
    LICENSE_LEN = 8

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (UserCreationForm.Meta.fields +
                  ("first_name", "last_name", "license_number",))

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != DriverLicenseUpdateForm.LICENSE_LEN:
            raise ValidationError(
                f"Ensure that license is "
                f"== {DriverLicenseUpdateForm.LICENSE_LEN} character long."
            )
        elif (license_number[:3] != license_number[:3].upper()
              or any(char.isdigit() for char in license_number[:3])):
            raise ValidationError(
                "Ensure that license number is correct"
            )
        elif not license_number[3:].isdigit():
            raise ValidationError("Invalid license number")
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
