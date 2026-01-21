from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Driver, Car


class BaseDriverForm(forms.ModelForm):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        first_3_chars = license_number[:3]
        last_5_chars = license_number[3:]
        if len(license_number) != 8:
            raise ValidationError(
                "License_Number must be 8 characters long")
        if not (first_3_chars.isalpha() and first_3_chars.isupper()):
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )
        if not last_5_chars.isdigit():
            raise ValidationError("Last 5 characters must be digits!")
        return license_number


class DriverLicenseForm(BaseDriverForm):
    class Meta:
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "license_number",
        )


class DriverLicenseUpdateForm(BaseDriverForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
