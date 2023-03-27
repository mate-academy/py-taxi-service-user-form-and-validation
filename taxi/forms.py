from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver


class DriverLicenseUpdateForm(forms.ModelForm):
    CORRECT_LENGHT = 8

    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.CORRECT_LENGHT:
            raise ValidationError(
                "Car license number must be 8 chars lenght"
            )
        if (
                not license_number[:3].isalpha()
                or license_number[:2] != license_number[:2].upper()
        ):
            raise ValidationError("First 3 symbols must be in uppercase")
        if not license_number[-5:].isdigit():
            raise ValidationError("Last 5 symbols must be digits")

        return license_number


class DriverForm(DriverLicenseUpdateForm, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (
            "username",
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):
        return super().clean_license_number()


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
