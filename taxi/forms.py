from django import forms
from django.contrib.auth import get_user_model

from taxi.models import Car, Driver


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise (forms.ValidationError
                   ("License number must be at least 8 characters long"))
        elif not (
                license_number[:3].isalpha()
        ):
            raise (forms.ValidationError
                   ("First 3 characters must be uppercase letters"))
        elif not license_number[-5:].isdigit():
            raise forms.ValidationError("Last 5 characters must be digits")
        return license_number


class CarCreationForm(forms.ModelForm):
    driver = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
