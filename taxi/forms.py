import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from taxi.models import Driver, Car


class DriverCreateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "first_name",
            "last_name",
            "license_number",
            "password1",
            "password2",
        ]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"].strip()
        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be exactly 8 characters long."
            )
        pattern = r"^[A-Z]{3}[0-9]{5}$"
        if not re.match(pattern, license_number):
            raise forms.ValidationError(
                "License number must start with 3 "
                "uppercase letters followed by 5 digits."
            )
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"].strip()
        if len(license_number) != 8:
            raise ValidationError(
                "License number must be exactly 8 characters long."
            )

        pattern = r"^[A-Z]{3}[0-9]{5}$"
        if not re.match(pattern, license_number):
            raise ValidationError(
                "License number must start with 3 "
                "uppercase letters followed by 5 digits."
            )
        return license_number


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
