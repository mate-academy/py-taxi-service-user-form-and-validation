from django import forms
from django.core.exceptions import ValidationError
from .models import Driver, Car


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["username", "full_name", "license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if (len(license_number) != 8
                or not license_number[:3].isalpha()
                or not license_number[:3].isupper()
                or not license_number[3:].isdigit()):
            raise ValidationError(
                "License number must consist of 3 uppercase "
                "letters followed by 5 digits.")
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if (len(license_number) != 8
                or not license_number[:3].isalpha()
                or not license_number[:3].isupper()
                or not license_number[3:].isdigit()):
            raise ValidationError(
                "License number must consist of 3 uppercase "
                "letters followed by 5 digits.")
        return license_number


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
