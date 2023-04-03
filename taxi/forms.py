from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseForm(forms.ModelForm):
    LENGTH = 8

    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != DriverLicenseForm.LENGTH:
            raise ValidationError(
                f"License number should be "
                f"{DriverLicenseForm.LENGTH} symbols"
            )

        if not license_number[:3].isupper():
            raise ValidationError("First 3 characters should be capitalized")

        if not license_number[:3].isalpha():
            raise ValidationError("First 3 characters should be letters")

        if not license_number[-5:len(license_number):1].isdigit():
            raise ValidationError("Last 5 characters should be digits")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
