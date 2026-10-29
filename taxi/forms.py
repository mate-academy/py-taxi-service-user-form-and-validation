
import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Car


Driver = get_user_model()


class LicenseNumberValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not re.fullmatch(r"[A-Z]{3}[0-9]{5}", license_number):
            raise ValidationError("Invalid license number format")

        return license_number


class DriverCreateForm(
    LicenseNumberValidationMixin,
    UserCreationForm,
):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = [
            "username",
            "first_name",
            "last_name",
            "license_number",
        ]


class DriverLicenseUpdateForm(
    LicenseNumberValidationMixin,
    forms.ModelForm,
):
    class Meta:
        model = Driver
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
