from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "license_number")


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("License number must consist of 8 digits.")
        if not license_number[:3].isalpha() or not license_number[:3].isupper():
            raise ValidationError("License number must begin with 3 uppercase latin letters.")
        if not license_number[3:].isnumeric():
            raise ValidationError("License number must end with 5 digits.")
        return license_number
