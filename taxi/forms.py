from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from taxi.models import Driver


def clean_license(license_number):
    if len(license_number) == 8:
        letter = all(letter.isupper() for letter in license_number[:3])
        digit = all(num.isdigit() for num in license_number[3:])
        if letter and digit:
            return license_number
    raise ValidationError("license number is not correct")


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", "first_name", "last_name", )

    def clean_license_number(self):
        return clean_license(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        return clean_license(self.cleaned_data["license_number"])


