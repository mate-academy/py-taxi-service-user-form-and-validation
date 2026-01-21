import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number",
        )

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        pattern = r"^[A-Z]{3}[0-9]{5}$"
        if not re.match(pattern, license_number):
            raise ValidationError(
                "License must consist of 3 uppercase letters "
                "followed by 5 digits (e.g., ABC12345)"
            )
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        pattern = r"^[A-Z]{3}[0-9]{5}$"
        if not re.match(pattern, license_number):
            raise ValidationError(
                "License must consist of 3 uppercase "
                "letters followed by 5 digits (e.g., ABC12345)"
            )
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
