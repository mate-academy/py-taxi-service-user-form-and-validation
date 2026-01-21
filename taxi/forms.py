from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from .models import Car, Driver


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("first_name", "last_name", "username", "license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError("Consist only of 8 characters")

        if (not license_number[:3].isalpha()
                or not license_number[:3].isupper()):
            raise forms.ValidationError(
                "First 3 characters are uppercase letters")

        if not license_number[3:].isdigit():
            raise forms.ValidationError("Last 5 characters are digits")

        return license_number


class DriverLicenseUpdateForm(ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError("Consist only of 8 characters")

        if (not license_number[:3].isalpha()
                or not license_number[:3].isupper()):
            raise forms.ValidationError(
                "First 3 characters are uppercase letters")

        if not license_number[3:].isdigit():
            raise forms.ValidationError("Last 5 characters are digits")

        return license_number
