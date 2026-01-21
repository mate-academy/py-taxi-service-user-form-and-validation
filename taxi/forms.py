from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django import forms
from taxi.models import Driver, Car


class LicenseValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if (
            len(license_number) == 8
            and license_number[0:3].isalpha()
            and license_number[0:3].isupper()
            and license_number[3:].isdigit()
        ):
            return license_number
        else:
            raise ValidationError(
                f"Not valid license number: {license_number}!"
            )


class DriverCreationForm(LicenseValidationMixin, UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )


class DriverLicenseUpdateForm(LicenseValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers",)
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
