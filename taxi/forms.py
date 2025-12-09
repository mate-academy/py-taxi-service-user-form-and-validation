from django import forms
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import get_user_model
from .models import Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise ValidationError(
                "Not allowed format"
            )
        return license_number


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
