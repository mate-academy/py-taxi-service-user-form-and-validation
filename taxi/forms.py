from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        first_3_chars = license_number[:3]
        last_5_chars = license_number[3:]

        if len(license_number) != DriverCreationForm.LEN_LICENSE_NUMBER:
            raise ValidationError(
                f"Length of lisense number must be "
                f"{DriverCreationForm.LEN_LICENSE_NUMBER} characters"
            )

        if not first_3_chars.isalpha():
            raise ValidationError(
                "First 3 characters of license_number must be letters"
            )

        if not last_5_chars.isnumeric():
            raise ValidationError(
                "Last 5 characters of license_number must be numbers"
            )

        return license_number


class DriverCreationForm(UserCreationForm):
    LEN_LICENSE_NUMBER = 8

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )

    def clean_license_number(self):
        return DriverLicenseUpdateForm.clean_license_number(self)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
