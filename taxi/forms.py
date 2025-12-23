from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import (
    Driver,
    Car
)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number: str = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "License number must consist of 8 characters"
            )
        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )
        if not license_number[-5:].isnumeric():
            raise ValidationError(
                "Last 5 characters must be digits"
            )
        return license_number


class DriverCreationForm(UserCreationForm, DriverLicenseUpdateForm):
    license_number = forms.CharField()

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number", "first_name", "last_name"
        )


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
