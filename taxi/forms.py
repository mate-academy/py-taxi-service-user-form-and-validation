from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car


class LicenseNumberValidation:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must contain exactly 8 characters."
            )

        if (not license_number[:3].isalpha()
                or not license_number[:3].isupper()):
            raise forms.ValidationError(
                "First 3 characters must be uppercase letters."
            )

        if not license_number[3:].isdigit():
            raise forms.ValidationError(
                "Last 5 characters must be digits."
            )

        return license_number


class DriverCreationForm(LicenseNumberValidation, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(LicenseNumberValidation, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
