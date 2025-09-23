from django.contrib.auth.forms import UserCreationForm
from django import forms
import re
from .models import Car
from taxi.models import Driver


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        min_length=8,
        widget=forms.TextInput(attrs={"placeholder": "ABC12345"}),
        label="License Number"
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number", "").upper()
        if not re.fullmatch(r"[A-Z]{3}[0-9]{5}", license_number):
            raise forms.ValidationError(
                "License number must be 3 uppercase letters followed by 5 digits."
            )
        return license_number


class DriverLicenseUpdateForm(forms.Form):
    license_number = forms.CharField(
        max_length=8,
        min_length=8,
        widget=forms.TextInput(attrs={"placeholder": "ABC12345"}),
        label="License Number"
    )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number", "").upper()

        if not re.fullmatch(r"[A-Z]{3}[0-9]{5}", license_number):
            raise forms.ValidationError(
                "License number must be 3 uppercase letters followed by 5 digits."
            )
        return license_number


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Drivers"
    )

    class Meta:
        model = Car
        fields = ["model", "drivers"]
