from django.contrib.auth.forms import UserCreationForm
import re
from django import forms

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        lic = self.cleaned_data.get("license_number", "").strip()
        if not re.match(r"^[A-Z]{3}\d{5}$", lic):
            raise forms.ValidationError(
                "License must be 3 uppercase letters + 5 digits"
            )
        return lic


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        lic = self.cleaned_data.get("license_number", "").strip()
        if not re.match(r"^[A-Z]{3}\d{5}$", lic):
            raise forms.ValidationError(
                "License must be 3 uppercase letters + 5 digits"
            )
        return lic


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
