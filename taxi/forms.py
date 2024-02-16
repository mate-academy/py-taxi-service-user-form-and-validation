from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = (
            "password",
            "last_login",
            "is_superuser",
            "groups",
            "user_permissions",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("Your license number must be 8 characters long")
        if not license_number[:3].isupper():
            raise ValidationError("Your license number must start with uppercase letters")
        if not license_number[3:].isdigit():
            raise ValidationError("Your license number must contain 5 digit characters")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
