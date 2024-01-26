from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("License number must be 8 characters long.")
        if not all(sign.isupper() for sign in license_number[:3]):
            raise ValidationError(
                "First 3 characters must be uppercase letters.")

        if not license_number[3:].isdigit():
            raise ValidationError("Last 5 characters must be digits.")

        return license_number


class DriverCreateForm(DriverLicenseUpdateForm):
    class Meta(DriverLicenseUpdateForm.Meta):
        fields = "__all__"
