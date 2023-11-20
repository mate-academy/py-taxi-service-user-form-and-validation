from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from taxi.models import Driver
from taxi.validators import license_number_validator


class DriverLicenseUpdateForm(ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        license_number_validator(license_number)
        return license_number


class DriverCreateForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        license_number_validator(license_number)
        return license_number
