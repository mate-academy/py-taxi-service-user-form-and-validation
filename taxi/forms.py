from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def check_license_number(license_number: str, max_length: int) -> str:
    if len(license_number) != max_length:
        raise ValidationError(f"Ensure that length of entered license "
                              f"number if equal to "
                              f"{DriverLicenseUpdateForm.MAX_LN_LENGTH}")

    if not (license_number[:3].isalpha()
            and license_number[:3].upper() == license_number[:3]
            and license_number[3:].isnumeric()):
        raise ValidationError("Ensure that entered license number is "
                              "correct! It must contain 3 letters in "
                              "uppercase and 5 numbers like example: "
                              "ABC12345")
    return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    MAX_LN_LENGTH = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = check_license_number(
            self.cleaned_data["license_number"],
            DriverLicenseUpdateForm.MAX_LN_LENGTH
        )
        return license_number


class DriverCreateForm(forms.ModelForm):
    MAX_LN_LENGTH = 8

    class Meta:
        model = Driver
        fields = ("username",
                  "password",
                  "license_number",
                  "first_name",
                  "last_name",
                  "email",)

    def clean_license_number(self) -> str:
        license_number = check_license_number(self.cleaned_data
                                              [
                                                  "license_number"
                                              ],
                                              DriverCreateForm.MAX_LN_LENGTH)
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
