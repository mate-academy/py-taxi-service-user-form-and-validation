from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number", ]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("License_number must be 8 characters long")
        if (not license_number[:3].isupper()
                or not license_number[:3].isalpha()):
            raise ValidationError(
                "Invalid license number: First 3 char. are uppercase letters"
            )
        if not license_number[3:].isdigit():
            raise ValidationError(
                "Invalid license number: Last 5 char. are digits"
            )
        return license_number


class DriverForm(DriverLicenseUpdateForm):
    class Meta:
        model = Driver
        fields = "__all__"


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Car
        fields = "__all__"
