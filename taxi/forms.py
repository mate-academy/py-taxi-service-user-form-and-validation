from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if not license_number:
            raise ValidationError("License is required")

        if len(license_number) != 8:
            raise ValidationError(
                "License must be exactly 8 characters."
            )

        if not license_number[:3].isupper():
            raise ValidationError(
                "First 3 characters must be uppercase letters."
            )

        if not license_number[3:].isdigit():
            raise ValidationError(
                "Last 5 characters must be digits."
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select drivers for this car"
    )

    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "model": forms.TextInput(attrs={"placeholder": "Enter car model"}),
        }

    def clean_model(self):
        model = self.cleaned_data.get("model")
        if not model:
            raise ValidationError("Model name is required")
        return model
