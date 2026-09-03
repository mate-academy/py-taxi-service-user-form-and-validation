import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Driver, Car


class LicenseNumberValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise ValidationError(
                "License number must consist of 8 characters: "
                "the first 3 must be uppercase letters "
                "and the last 5 must be digits."
            )

        return license_number


class DriverCreationForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
