from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number", "first_name", "last_name"
        )


class DriverUpdateLicenseForm(forms.ModelForm):
    LICENSE_NUMBER = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != DriverUpdateLicenseForm.LICENSE_NUMBER:
            raise ValidationError(
                "Len license number must be"
                f" {DriverUpdateLicenseForm.LICENSE_NUMBER}!"
            )

        if not license_number[:3].isupper():
            raise ValidationError("First 3 letter must be upper case!")

        if not license_number[4:].isdigit():
            raise ValidationError("Last 5 symbol must be numbers!")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer",)
