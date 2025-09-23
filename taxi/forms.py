from django import forms
import re
from .models import Car
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


Driver = get_user_model()


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get(
            "license_number", ""
        ).upper().strip()
        if not re.fullmatch(r"[A-Z]{3}[0-9]{5}", license_number):
            raise forms.ValidationError(
                "License number must be 3"
                " uppercase letters followed by 5 digits."
            )
        return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = [
            "first_name",
            "last_name",
            "license_number",
            "username",
            "password",
        ]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number", "").upper()
        if not re.fullmatch(r"[A-Z]{3}[0-9]{5}", license_number):
            raise forms.ValidationError(
                "License number must be 3"
                " uppercase letters followed by 5 digits."
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
