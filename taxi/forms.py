from django import forms
from django.core.exceptions import ValidationError
from .models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("License must be exactly "
                                  "8 characters long")
        if (not license_number[:3].isalpha()
                or not license_number[:3].isupper()):
            raise ValidationError("First 3 characters "
                                  "must be uppercase letters")
        if not license_number[3:].isdigit():
            raise ValidationError("Last 5 characters must be digits")
        return license_number


class DriverCreationForm(DriverLicenseUpdateForm):
    class Meta(DriverLicenseUpdateForm.Meta):
        fields = ["username", "first_name", "last_name", "license_number"]


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple
        }
