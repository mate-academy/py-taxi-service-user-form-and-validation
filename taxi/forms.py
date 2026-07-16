from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from taxi.models import Driver


class LicenceNumberValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if (
                len(license_number) == 8
                and license_number[:3].isalpha()
                and license_number[:3].isupper()
                and license_number[3:].isdigit()
        ):
            return license_number
        else:
            raise forms.ValidationError(
                "licence_number is not valid. "
                "Please ensure that licence_number: \n"
                "Consist only of 8 characters \n"
                "First 3 characters are uppercase letters \n"
                "Last 5 characters are digits")


class DriverUpdateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name",)


class DriverCreateForm(LicenceNumberValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(LicenceNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)
