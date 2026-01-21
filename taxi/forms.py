from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )
        widgets = {
            "license_number":
                forms.TextInput(
                    attrs={"placeholder": "ABC12345"}
                )
        }

    def clean_license_number(self):
        data = self.cleaned_data["license_number"]
        if len(data) != 8:
            raise ValidationError(
                "License number must consist of exactly 8 characters."
            )
        if not data[:3].isupper():
            raise ValidationError(
                "The first three characters must be uppercase letters."
            )
        if not data[:3].isalpha():
            raise ValidationError(
                "The first three characters must be letters."
            )
        if not data[3:].isdigit():
            raise ValidationError(
                "The last five characters must be digits."
            )
        return data


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
