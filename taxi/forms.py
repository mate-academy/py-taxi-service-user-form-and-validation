import re

from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not bool(re.match(r"^[A-Z]{3}\d{5}$", license_number)):
            raise forms.ValidationError("The driving licence number "
                                        "must consist of capital "
                                        "letters and numbers only")
        return license_number
