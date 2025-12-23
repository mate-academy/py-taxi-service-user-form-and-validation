from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise ValidationError("Must be exactly 8 characters long")

        if (
                not license_number[:3].isupper() or not license_number[:3].isalpha()  # NOQA E501
        ):
            raise ValidationError("First three characters must be uppercase letters")  # NOQA E501

        if not license_number[3:].isdigit():
            raise ValidationError("Must be a number")

        return license_number
