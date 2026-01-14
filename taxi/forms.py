from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Car

Driver = get_user_model()

class DriverForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = ["username", "first_name", "last_name", "license_number"]

    def clean_license_number(self):
        license = self.cleaned_data["license_number"]
        if len(license) != 8 or not license[:3].isupper() or not license[3:].isdigit():
            raise ValidationError("License must be 3 uppercase letters followed by 5 digits.")
        return license


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license = self.cleaned_data["license_number"]
        if len(license) != 8 or not license[:3].isupper() or not license[3:].isdigit():
            raise ValidationError("License must be 3 uppercase letters followed by 5 digits.")
        return license


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
        widgets = {
            "drivers": forms.CheckboxSelectMultiple()
        }
