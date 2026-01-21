from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    NUMBER_LENGTH = 8
    EXAMPLE = "AAA12345"

    class Meta:
        model = Driver
        fields = ("first_name", "last_name", "license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not license_number:
            raise ValidationError("License number is required.")

        if len(license_number) != DriverLicenseUpdateForm.NUMBER_LENGTH:
            raise ValidationError(
                f"Ensure that value is {DriverLicenseUpdateForm.NUMBER_LENGTH}"
            )

        if not license_number[:3].isalpha():
            raise ValidationError(
                "Ensure that first three symbols is letters. "
                f"Example: {DriverLicenseUpdateForm.EXAMPLE}"
            )

        if not license_number[:3].isupper():
            raise ValidationError(
                "Ensure that first three symbols in uppercase."
                f"Example: {DriverLicenseUpdateForm.EXAMPLE}"
            )

        if not license_number[3:].isnumeric():
            raise ValidationError(
                "Ensure that last five symbols are numbers."
                f"Example: {DriverLicenseUpdateForm.EXAMPLE}"
            )

        return license_number


class DriverCreationForm(UserCreationForm, DriverLicenseUpdateForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name",
                                                 "last_name",
                                                 "license_number")


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Car
        fields = "__all__"
