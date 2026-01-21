from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car


class LicenseValidationMixin:
    def clean_license_number(self) -> str:
        license_number = self.cleaned_data.get("license_number")
        if (
                license_number[:3].isalpha()
                and license_number[:3].isupper()
                and license_number[3:].isdigit()
                and len(license_number) == 8
        ):
            return license_number
        else:
            raise forms.ValidationError(
                "License number must consist of "
                "3 uppercase letters followed by 5 digits."
            )


class DriverCreationForm(LicenseValidationMixin, UserCreationForm):
    license_number = forms.CharField(max_length=8, required=True)

    class Meta:
        model = get_user_model()
        fields = (
            "license_number", "username", "password1", "password2",
            "email", "first_name", "last_name"
        )


class DriverLicenseUpdateForm(LicenseValidationMixin, forms.ModelForm):
    license_number = forms.CharField(max_length=8, required=True)

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
