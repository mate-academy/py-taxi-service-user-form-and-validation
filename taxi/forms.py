from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator
from django.db import models

from taxi.models import Driver, Car


class LicenseValidationMixin:
    CHARACTERS = 8
    UPPERCASE_LETTERS = 3
    DIGITS = 5

    def validate_license_number(self, license_number):
        if (len(license_number) != self.CHARACTERS
                or not license_number[:self.UPPERCASE_LETTERS].isalpha()
                or not license_number[:self.UPPERCASE_LETTERS].isupper()
                or not license_number[-self.DIGITS:].isdigit()):
            raise forms.ValidationError(
                f"Make sure the license number is "
                f"{self.CHARACTERS} characters long, "
                f"first {self.UPPERCASE_LETTERS} characters are uppercase"
                f"letters, and last {self.DIGITS} characters are digits."
            )
        return license_number


class DriverCreationForm(UserCreationForm, LicenseValidationMixin):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (UserCreationForm.Meta.fields
                  + ("first_name", "last_name", "license_number"))

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return self.validate_license_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm, LicenseValidationMixin):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return self.validate_license_number(license_number)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
