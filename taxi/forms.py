from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
            "email",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    DRIVER_LICENSE_LEN = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != self.DRIVER_LICENSE_LEN:
            raise ValidationError("license number must contain 8 characters.")
        if not (
            license_number[0:3].isalpha()
            and license_number[0:3].isupper()
        ):
            raise ValidationError("first 3 characters must be capital letters")

        if not license_number[3:].isdigit():
            raise ValidationError("last 5 characters must be digits")
        return license_number
