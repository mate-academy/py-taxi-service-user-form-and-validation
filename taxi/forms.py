import re

from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import forms

from taxi.models import Driver


class DriverLicenseUpdateForm(UserCreationForm):
    liecense_number = forms.CharField(
        max_lenght=8,
        required=True,
        help_text="Liense nnumber must be 3 uppercase letters followed by 5 digits",
    )
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("username", "password1", "password2", "license_number")


    def clen_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.match(r'^[A-Z]{3}\d{5}$',license_number):
            raise ValidationError("Invalid license number")
        return license_number