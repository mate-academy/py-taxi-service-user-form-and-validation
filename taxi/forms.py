from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    COUNT_CHARACTERS_LICENSE = 8
    COUNT_FIRST_LETTERS = 3
    COUNT_LAST_DIGITS = 5

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number"
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        is_valid_len = len(license_number) == self.COUNT_CHARACTERS_LICENSE
        is_last_digits = (
            license_number[self.COUNT_CHARACTERS_LICENSE
                           - self.COUNT_LAST_DIGITS:].isdigit()
        )
        is_first_letters = (
            license_number[:self.COUNT_FIRST_LETTERS].isalpha()
        )

        errors = ""

        if not is_valid_len:
            errors += (
                f"Consist only of {self.COUNT_CHARACTERS_LICENSE} characters. "
            )
        if is_first_letters:
            is_first_letters = (
                license_number[:self.COUNT_FIRST_LETTERS]
                == license_number[:self.COUNT_FIRST_LETTERS].upper()
            )
        if not is_first_letters:
            errors += (
                f"First {self.COUNT_FIRST_LETTERS} "
                "characters are uppercase letters. "
            )
        if not is_last_digits:
            errors += f"Last {self.COUNT_LAST_DIGITS} characters are digits. "
        if errors:
            raise ValidationError(errors)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    COUNT_CHARACTERS_LICENSE = 8
    COUNT_FIRST_LETTERS = 3
    COUNT_LAST_DIGITS = 5

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        return DriverCreationForm.clean_license_number(self)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
