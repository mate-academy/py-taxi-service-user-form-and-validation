from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver


def clean_license(license_number):
    if len(license_number) == 8:
        letter = all(letter.isupper() for letter in license_number[:3])
        num = all(num.isdigit() for num in license_number[3:])
        if letter and num:
            return license_number
    raise ValidationError("license number is not correct")


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Driver
        fields = (UserCreationForm.Meta.fields
                  + ("first_name", "last_name", "license_number"))

    def clean_license_number(self):
        return clean_license(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        return clean_license(self.cleaned_data["license_number"])
