from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms

from .models import Driver, Car


class LicenseNumberValidator:
    def clean_license_number(self):
        license_number: str = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "License should consist 8 characters"
            )
        if (
            not license_number[:3].isupper()
            or not license_number[:3].isalpha()
        ):
            raise ValidationError(
                "First 3 characters should be uppercase letters"
            )
        if not license_number[3:].isdigit():
            raise ValidationError(
                "Last 5 characters should be digits"
            )
        return license_number


class DriverCreationForm(LicenseNumberValidator, UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email"
        )


class DriverLicenseUpdateForm(LicenseNumberValidator, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Car
        fields = "__all__"
