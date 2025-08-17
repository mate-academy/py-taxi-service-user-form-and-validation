from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("Does not consist of 8 characters")
        if not (
                license_number[:3].isalpha() and license_number[:3].isupper()
        ):
            raise ValidationError(
                "First 3 characters are not uppercase letters"
            )
        if not license_number[3:].isdigit():
            raise ValidationError("Last 5 characters are not digits")

        return license_number


class DriverLicenseCreateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = "__all__"

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("Does not consist of 8 characters")
        if not (
                license_number[:3].isalpha() and license_number[:3].isupper()
        ):
            raise ValidationError(
                "First 3 characters are not uppercase letters"
            )
        if not license_number[3:].isdigit():
            raise ValidationError("Last 5 characters are not digits")

        return license_number


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
