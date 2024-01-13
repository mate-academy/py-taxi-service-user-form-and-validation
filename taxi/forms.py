from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from taxi.models import Driver

from typing import Any


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self) -> Any:
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("License must be 8 characters long!")
        if (not license_number[:3].isupper()
                or not license_number[:3].isalpha()):
            raise ValidationError("First three character must be upper case!")
        if not license_number[3:].isdigit():
            raise ValidationError("Last five characters should be digit!")
        return license_number
