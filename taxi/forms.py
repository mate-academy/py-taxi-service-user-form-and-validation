from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }


class LicenseNumberValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        first_part = license_number[:3]
        second_part = license_number[3:]
        if (
                len(license_number) == 8
                and first_part.upper() == first_part
                and first_part.isalpha()
                and second_part.isdigit()):
            return license_number
        raise ValidationError("Ensure that you enter a valid license number.")


class DriverCreationForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta:
        model = Driver
        fields = (UserCreationForm.Meta.fields
                  + ("license_number", "first_name", "last_name"))


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, UserChangeForm):
    class Meta:
        model = Driver
        fields = ("license_number",)
