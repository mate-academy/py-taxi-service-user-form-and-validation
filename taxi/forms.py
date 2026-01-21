from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver
from taxi.validators import validate_license_number


class DriverCreateForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name"
        )

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]

        return validate_license_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    CONSIST_CHARACTER = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]

        return validate_license_number(license_number)
