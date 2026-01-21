import re

from django import forms
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm

from taxi.models import Driver, Car, Manufacturer


class LicenseNumberValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise ValidationError(
                "License number must be in format:"
                " 3 uppercase letters followed by 5 digits."
            )

        return license_number


class DriverCreationForm(UserCreationForm, LicenseNumberValidationMixin):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(ModelForm, LicenseNumberValidationMixin):
    class Meta:
        model = Driver
        fields = ("license_number", )


class CarForm(ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
